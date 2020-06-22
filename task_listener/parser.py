import json

from task_listener.exceptions import ParsingError
from task_listener.log_writer import write as write_log
from task_listener.models.ticket import Ticket
from task_listener.connector import get_internal_ticket_data


def get_tickets_from_inbox_data(inbox_data):
    write_log('Starting parsing new received data...')
    tickets = []
    dict_inbox_data = json.loads(inbox_data)
    for i, ticket_source in enumerate(dict_inbox_data['data']):
        ticket = Ticket()
        ticket.subject = splitting(source=ticket_source[1], from_phrase='\'>', count_from=1, to_phrase='&nbsp')
        ticket.ticket_id = splitting(source=ticket_source[2], from_phrase='title=\'', to_phrase='\'>')
        ticket.link = splitting(source=ticket_source[2], from_phrase='<a href=\'', to_phrase='\' title=')
        ticket.assignee_name = splitting(source=ticket_source[9], from_phrase='>', count_from=2, to_phrase='</span>')
        ticket.reporter = splitting(source=ticket_source[6], from_phrase='\'>', count_from=2, to_phrase='<span')
        ticket.last_activity = splitting(source=ticket_source[10], from_phrase='">', to_phrase='</span>')
        ticket.topic = ticket_source[3]
        ticket.department = ticket_source[4]
        ticket.ib_name = ticket_source[7]
        ticket.brands = ticket_source[8]
        ticket.status, ticket.last_message = get_status_and_last_message(ticket.link)
        tickets.append(ticket)
    write_log('Parsing data is done')
    return tickets


def splitting(*, source, from_phrase, count_from=1, to_phrase, count_to=1):
    maxsplit_from = count_from
    count_to -= 1
    try:
        return str.split(str.split(source, from_phrase, maxsplit=maxsplit_from)[count_from], to_phrase)[count_to]
    except IndexError:
        raise ParsingError(splitting_part=f'{from_phrase}:{to_phrase}')


def get_status_and_last_message(url):
    internal_data = get_internal_ticket_data(url)
    status = splitting(source=internal_data, from_phrase='id="ticketStatus" value="', to_phrase='">')
    last_message = splitting(source=internal_data, from_phrase='Last message:</b></td>   <td>', to_phrase='</td></tr>')
    if 'email-protection' in last_message:
        last_message = 'Undefined'
    return status, last_message


def get_status_and_last_activity(url):
    internal_data = get_internal_ticket_data(url)
    status = splitting(source=internal_data, from_phrase='id="ticketStatus" value="', to_phrase='">')
    last_activity = splitting(source=internal_data, from_phrase='Last response: </b> ', to_phrase='\n')
    return status, last_activity
