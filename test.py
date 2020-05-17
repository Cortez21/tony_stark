from datetime import datetime
from hashlib import sha256

from task_listener.connector import get_inbox_data
from task_listener.database.checksum_manager import insert_checksum

source = get_inbox_data()

checksum = sha256(source.encode('utf-8'))

print(checksum.hexdigest())

insert_checksum(checksum.hexdigest())