from hashlib import sha256
from pprint import pprint

from task_listener import parser, connector
from task_listener.config_reader import get_reaction
from task_listener.database.assignee_manager import get_all_assignee
from task_listener.database.checksum_manager import get_last_checksum, insert_checksum
from task_listener.log_writer import write as write_log
from task_listener.message_formatter import get_answered, get_initial, get_reassigned
from task_listener.parser import get_status_and_last_activity
from task_listener.slack import send_message, remove_reaction, change_reaction
from task_listener.database.ticket_manager import check_if_ticket_exist, insert_ticket, get_ticket, \
    update_answered_ticket as update_ticket, update_assignee, get_opened
from task_listener.database.notification_manager import insert_notification, get_message_ts_list
from task_listener.models.notification import Notification


def get_channel_names_list():
    assignee_list = get_all_assignee()
    return [assignee.assignee_name.lower() for assignee in assignee_list]


def check_if_changed(source):
    write_log('Checking incoming hash sum')
    hashed_source = sha256(source.encode('utf-8')).hexdigest()
    print(hashed_source)
    if hashed_source != get_last_checksum():
        print(f'Detected some changing in inbox data, save new checksum {hashed_source} in DB')
        insert_checksum(hashed_source)
        return True
    else:
        message = 'Nothing changed in inbox'
        print(message)
        write_log(message)
        return False


def main():
    fresh_tickets_data = connector.get_inbox_data()
    if check_if_changed(fresh_tickets_data):
        tickets = parser.get_tickets_from_inbox_data(fresh_tickets_data)
        handle_incoming(tickets)
        opened_list = get_opened()
        incoming_tickets_ids_list = [ticket.ticket_id for ticket in tickets]
        for opened_ticket in opened_list:
            if opened_ticket.ticket_id not in incoming_tickets_ids_list:
                loaded_status, loaded_activity = get_status_and_last_activity(opened_ticket.link)
                print(loaded_status, opened_ticket.status)
                if loaded_status != opened_ticket.status:
                    opened_ticket.status, opened_ticket.last_activity = loaded_status, loaded_activity
                    update_ticket(opened_ticket)
                    for message_ts in get_message_ts_list(opened_ticket):
                        change_reaction(message_ts, get_reaction(opened_ticket.status))


def handle_incoming(incoming_tickets):
    for incoming_ticket in incoming_tickets:
        incoming_ticket_id = incoming_ticket.ticket_id
        if check_if_ticket_exist(incoming_ticket_id):
            write_log(f'Ticket {incoming_ticket.ticket_id} already exist in DB. Loading current...')
            stored_ticket = get_ticket(incoming_ticket_id)
            if incoming_ticket.last_message.lower() != stored_ticket.last_message.lower() \
                    and incoming_ticket.last_message.lower() not in get_channel_names_list():
                update_ticket(incoming_ticket)
                initialize_notification(get_answered, incoming_ticket, stored_ticket)
            elif incoming_ticket.assignee_name.lower() != stored_ticket.assignee_name.lower():
                update_assignee(incoming_ticket)
                initialize_notification(get_reassigned, incoming_ticket, stored_ticket)
            elif incoming_ticket.last_message.lower() != stored_ticket.last_message.lower():
                update_ticket(incoming_ticket)
            elif incoming_ticket.status != stored_ticket.status:
                for message_ts in get_message_ts_list(stored_ticket):
                    remove_reaction(message_ts, get_reaction(stored_ticket.status))
                update_ticket(incoming_ticket)
        else:
            insert_ticket(incoming_ticket)
            initialize_notification(get_initial, incoming_ticket, get_ticket(incoming_ticket.ticket_id))


def initialize_notification(template_method, incoming_ticket, stored_ticket):
    message_template = template_method(incoming_ticket, stored_ticket)
    response = send_message(message_template)
    save_notification(incoming_ticket.ticket_id, response, True if template_method.__name__ == 'get_initial' else False)


def save_notification(incoming_ticket_id, response, initial):
    if response.status_code == 200 and response.json()['ok']:
        notification = Notification(
            {'id': None, 'ticket_id': get_ticket(incoming_ticket_id).id, 'initial': initial,
             'slack_ts': response.json()['ts'],
             'team_id': response.json()['message']['team'], 'channel': response.json()['channel']})
        insert_notification(notification)


if __name__ == '__main__':
    main()
