from task_listener.log_writer import write as write_log
from task_listener.models.notification import Notification
from task_listener.database.psql_connection import PSQLConnection


def insert_notification(notification):
    write_log(f'Saving {notification.slack_ts} into DB...')
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"""insert into notification values (
            (select nextval('notification_sequence')),
            '{notification.ticket_id}',
            {notification.initial},
            '{notification.slack_ts}',
            '{notification.team_id}',
            '{notification.channel}')""")
    write_log(' done', is_new_line=False)


def get_initial(stored_ticket):
    write_log(f'Getting initial notification for {stored_ticket.ticket_id} from DB...')
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"""select * from notification where
        ticket_id = {stored_ticket.id} and
        initial = True
        """)
        response = cursor.fetchall()
    result_notification = Notification(response[0])
    write_log(f' fail' if not response else f' done (found {result_notification.slack_ts})', is_new_line=False)
    return result_notification


def get_message_ts_list(stored_ticket):
    write_log(f'Getting notifications list for {stored_ticket.ticket_id} in DB...')
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"""select slack_ts from notification where
        ticket_id = {stored_ticket.id}
        """)
        result = cursor.fetchall()
    write_log(f'{" done" if result else " fail"}', is_new_line=False)
    return result
