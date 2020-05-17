from task_listener.models.notification import Notification
from task_listener.database.psql_connection import PSQLConnection


def insert_notification(notification):
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"""insert into notification values (
            (select nextval('notification_sequence')),
            '{notification.ticket_id}',
            {notification.initial},
            '{notification.slack_ts}',
            '{notification.team_id}',
            '{notification.channel}')""")


def get_initial(stored_ticket):
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"""select * from notification where
        ticket_id = {stored_ticket.id} and
        initial = True
        """)
        response = cursor.fetchall()
    return Notification(response[0])


def get_message_ts_list(stored_ticket):
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"""select slack_ts from notification where
        ticket_id = {stored_ticket.id}
        """)
        result = cursor.fetchall()
    return result
