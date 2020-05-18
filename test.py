from datetime import datetime
from hashlib import sha256

from task_listener.connector import get_inbox_data
from task_listener.database.checksum_manager import insert_checksum
from task_listener.slack import send_message

print(send_message('Hi').text)