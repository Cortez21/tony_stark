import task_listener.launch
from time import sleep

while True:
    task_listener.launch.main()
    print("Iteration turned...")
    sleep(60)
