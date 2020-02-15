from task_listener.log_writer import write as write_log


def create_for_new(ticket_data):
    write_log('Starting formatting the message about new ticket...')
    message_body = """
    Created new ticket: {}
    Title: {}
    By: {}
    Assignee: {}
    Link: {}
    """.format(ticket_data['ticket_id'], ticket_data['title'], ticket_data['created_by'], ticket_data['assigned_to'],
               ticket_data['link'])
    write_log('Message is formatted - returning into main script')
    return message_body


def create_for_exist(ticket_data, time_passed):
    write_log('Starting formatting the message about reopened ticket...')
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
    write_log('Message is formatted - returning into main script')
    return message_body
