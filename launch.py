import task_listener.launch
from time import sleep

from task_listener.log_writer import write

print('Starting bot...')

while True:
    try:
        task_listener.launch.main()
    except Exception as exc:
        write(exc.__dict__)
    print("Iteration turned...")
    write('*' * 45)
    sleep(10)
