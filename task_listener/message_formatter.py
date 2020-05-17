from task_listener.database.assignee_manager import get_assignee
from task_listener.database.ticket_manager import get_ticket
from task_listener.log_writer import write as write_log
from task_listener.config_reader import get_department_icon as get_icon, get_default_assignee
from task_listener.slack import get_permalink
from task_listener.database.notification_manager import get_initial as get_initial_notification


def get_initial(incoming_ticket, _):
    ticket = get_ticket(incoming_ticket.ticket_id)
    assignee = get_assignee(ticket.assignee_name)
    message_template = f"""
    <{'@' + assignee.slack_id if assignee else get_default_assignee()}>
    Created new ticket <{ticket.link}|{ticket.ticket_id}>
    Subject: `{ticket.subject}`
    By: {ticket.reporter}
    Assignee: {ticket.assignee_name}
    Department: {ticket.department} {get_icon(ticket.department)}
    Brand: *{ticket.brands}*
    """
    return message_template


def get_answered(incoming_ticket, stored_ticket):
    assignee = get_assignee(stored_ticket.assignee_name)
    message_template = f"""
        <{'@' + assignee.slack_id if assignee else get_default_assignee()}>
        {incoming_ticket.last_message} answered in ticket
        {get_initial_permalink(stored_ticket)}
        """
    return message_template


def get_initial_permalink(stored_ticket):
    initial_message = get_initial_notification(stored_ticket)
    permalink = get_permalink(initial_message.slack_ts)
    return permalink


def get_reassigned(incoming_ticket, stored_ticket):
    assignee = get_assignee(incoming_ticket.assignee_name)
    message_template = f"""
            <{'@' + assignee.slack_id if assignee else get_default_assignee()}>
            Ticket reassigned to {incoming_ticket.assignee_name}
            {get_initial_permalink(stored_ticket)}
            """
    return message_template
