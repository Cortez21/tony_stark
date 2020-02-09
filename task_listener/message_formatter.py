def create_for_new(ticket_data):
    message_body = """
    Created new ticket: {}
    Title: {}
    By: {}
    Assignee: {}
    Link: {}
    """.format(ticket_data['ticket_id'], ticket_data['title'], ticket_data['created_by'], ticket_data['assigned_to'],
               ticket_data['link'])
    return message_body


def create_for_exist(ticket_data, time_passed):
    time_passed_message = ''
    for key in time_passed:
        time_passed_message = time_passed_message + '{} {} '.format(time_passed[key], key)
    message_body = """
    Ticket {} was re-opened
    Title: {}
    By: {}
    Assignee: {}
    Time passed: {}
    Link: {}
    """.format(ticket_data['ticket_id'], ticket_data['title'], ticket_data['created_by'], ticket_data['assigned_to'],
               time_passed_message, ticket_data['link'])
    return message_body
