from task_listener.database.psql_connection import PSQLConnection
from datetime import datetime


def insert_checksum(checksum_string):
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"insert into inbox_checksum values ('{datetime.now()}', '{checksum_string}')")


def get_last_checksum():
    print('Trying to DB connect...')
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"SELECT checksum FROM inbox_checksum ORDER BY date DESC LIMIT 1")
        response = cursor.fetchall()
        return response[0]['checksum'] if response else None
