from task_listener.database.psql_connection import PSQLConnection
from task_listener.models.assignee import Assignee


def get_assignee(assignee_name):
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"SELECT * FROM assignee WHERE assignee_name = '{assignee_name}'")
        response = cursor.fetchall()
        return Assignee(response[0]) if len(response) > 0 else None


def get_all_assignee():
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"SELECT * FROM assignee")
        response = cursor.fetchall()
        assignee_list = list()
        for assignee_data in response:
            assignee_list.append(Assignee(assignee_data))
        return assignee_list
