import psycopg2
import psycopg2.extras
from task_listener.config_reader import get_psql_credentials as get_credentials


class PSQLConnection:
    conn = None

    def __init__(self, db_name):
        credentials = get_credentials()
        host = credentials['host']
        user = credentials['user']
        password = credentials['password']
        port = credentials['port']
        self.conn = psycopg2.connect(host=host, port=port, database=db_name, user=user,
                                     password=password)
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
