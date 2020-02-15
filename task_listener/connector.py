import requests
from task_listener import data_keeper
from task_listener.log_writer import write as write_log


def get_inbox_data():
    cookies = data_keeper.get_cookies('task_listener/cookies')
    url = 'https://tickets.smcompany.co/filter?segment=%2Fticket%2Finbox&_=1581179004413'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': '{}'.format(cookies)
    }
    write_log('Connecting to ticket-system...')
    response = requests.get(url=url, headers=headers).text
    if response:
        write_log('Data from ticket-system received')
    return response

