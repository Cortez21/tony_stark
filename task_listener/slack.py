import requests
from task_listener.data_keeper import get_webhook_token as get_token
from task_listener.log_writer import write as write_log


def send_message(message):
    write_log('Sending message')
    headers = {
        'Content-type': 'application/json'
    }
    data = '{"text":"%s"}' % message
    data = str.encode(data, encoding='utf-8')
    url = 'https://hooks.slack.com/services/{}'.format(get_token())
    requests.post(url=url, headers=headers, data=data)