import requests
from task_listener import data_keeper


def get_inbox_data():
    cookies = data_keeper.get_cookies('task_listener/cookies')
    url = 'https://tickets.smcompany.co/filter?segment=%2Fticket%2Finbox&_=1581179004413'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': '{}'.format(cookies)
    }
    return requests.get(url=url, headers=headers).text

