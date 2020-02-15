import requests
from task_listener.log_writer import write as write_log


def send_message_to_me(message):
    write_log('Sending message to me')
    headers = {
        'Content-type': 'application/json'
    }
    data = '{"text":"%s"}' % message
    data = str.encode(data, encoding='utf-8')
    url = 'https://hooks.slack.com/services/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'
    requests.post(url=url, headers=headers, data=data)


def send_message_to_support_channel(message):
    write_log('Sending message to support channel')
    headers = {
        'Content-type': 'application/json'
    }
    data = '{"text":"%s"}' % message
    data = str.encode(data, encoding='utf-8')
    url = 'https://hooks.slack.com/services/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'
    requests.post(url=url, headers=headers, data=data)