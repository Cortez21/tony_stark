from task_listener.database.psql_connection import PSQLConnection
from datetime import datetime


def insert_checksum(checksum_string):
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"insert into inbox_checksum values ('{datetime.now()}', '{checksum_string}')")


def get_last_checksum():
    with PSQLConnection('ticket_system_bot') as connection:
        cursor = connection.get_cursor()
        cursor.execute(f"SELECT checksum, MAX(date) FROM inbox_checksum GROUP BY checksum, date LIMIT 1")
        response = cursor.fetchall()
        return response[0]['checksum'] if response else None
