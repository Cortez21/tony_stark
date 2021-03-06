from task_listener.database.psql_connection import PSQLConnection
from task_listener.log_writer import write as write_log
from task_listener.models.ticket import Ticket
from task_listener.database.assignee_manager import get_assignee


def check_if_ticket_exist(ticket_id):
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"SELECT * FROM ticket WHERE ticket_id = '{ticket_id}'")
        result = cursor.fetchall()
        return bool(result)


def get_ticket(ticket_id):
    write_log(f'Getting {ticket_id} ticket from DB...')
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"SELECT * FROM ticket WHERE ticket_id = '{ticket_id}'")
        response = cursor.fetchall()
        write_log(' done' if len(response) > 0 else ' nothing to get', is_new_line=False)
        return Ticket(response[0]) if len(response) > 0 else None


def insert_ticket(ticket):
    write_log(f'Inserting {ticket.ticket_id} ticket into DB')
    assignee_obj = get_assignee(ticket.assignee_name)
    ticket.subject = ticket.subject.replace('\'', '"')
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(
            f"""insert into ticket values ((
            select nextval('tickets_sequence')),
            '{ticket.ticket_id}',
            '{ticket.subject}',
            '{ticket.topic}',
            '{ticket.department}',
            '{ticket.reporter}',
            '{ticket.ib_name}',
            '{ticket.brands}',
            '{ticket.assignee_name}',
            {assignee_obj.id if assignee_obj else 'Null'},
            '{ticket.status}',
            '{ticket.link}',
            '{ticket.last_activity}',
            '{ticket.last_message}')""")


def update_answered_ticket(ticket):
    write_log(f'Update status, last_activity and last_message for ticket {ticket.ticket_id} in DB')
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"""update ticket set 
        status = '{ticket.status}',
        last_activity = '{ticket.last_activity}',
        last_message = '{ticket.last_message}'
        where ticket_id = '{ticket.ticket_id}'
        """)


def update_assignee(incoming_ticket):
    write_log(f'Update assignee for ticket {incoming_ticket.ticket_id} in DB: ')
    assignee = get_assignee(incoming_ticket.assignee_name)
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"""update ticket set 
        assignee_name = '{incoming_ticket.assignee_name}',
        assignee_id = {assignee.id if assignee else 'Null'}
        where ticket_id = '{incoming_ticket.ticket_id}'
        """)
    write_log('done', is_new_line=False)


def get_opened():
    write_log('Loading all opened ticket from DB...')
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"SELECT * FROM ticket WHERE status = 'open'")
        response = cursor.fetchall()
        ticket_list = list()
        for ticket in response:
            ticket_list.append(Ticket(ticket))
        write_log(f'found {len(ticket_list)} opened ticket in DB at the moment', is_new_line=False)
        return ticket_list
