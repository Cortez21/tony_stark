import json


def get_tickets_from_inbox_data(inbox_data):
    tickets = []
    dict_inbox_data = json.loads(inbox_data)
    for ticket_source in dict_inbox_data['data']:
        ticket_dict = {
            'title': splitting(source=ticket_source[1], from_phrase='\'>', count_from=2, to_phrase='&nbsp'),
            'ticket_id': splitting(source=ticket_source[2], from_phrase='title=\'', to_phrase='\'>'),
            'link': splitting(source=ticket_source[2], from_phrase='<a href=\'', to_phrase='\' title='),
            'assigned_to': splitting(source=ticket_source[9], from_phrase='<span>', to_phrase='</span>'),
            'created_by': splitting(source=ticket_source[6], from_phrase='<span>', to_phrase='</span>')
        }
        tickets.append(ticket_dict)
    return tickets


def splitting(*, source, from_phrase, count_from=1, to_phrase, count_to=1):
    count_to -= 1
    return str.split(str.split(source, from_phrase)[count_from], to_phrase)[count_to]
