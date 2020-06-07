from time import sleep

import requests

from task_listener.config_reader import get_slack_token as get_token, get_slack_channel as get_channel, get_bot_id
from task_listener.log_writer import write as write_log


def send_message(message):
    write_log('Sending message to slack channel...')
    url = f'https://slack.com/api/chat.postMessage?token={get_token()}&channel={get_channel()}&text={message}&pretty=1'
    response = requests.post(url)
    write_log('Success' if response.status_code == 200 and response.json()['ok'] else f'Fail ({response.json()["error"]})', is_new_line=False)
    return response


def get_permalink(message_ts):
    write_log(f'Getting permalink for {message_ts}...')
    url = f'https://slack.com/api/chat.getPermalink?token={get_token()}&channel={get_channel()}&message_ts={message_ts}&unfurl_links=true&pretty=1'
    response = requests.get(url)
    write_log('Success' if response.status_code == 200 and response.json()['ok'] else 'Fail', is_new_line=False)
    return response.json()['permalink']


def add_reaction(message_ts, reaction):
    write_log(f'Adding {reaction} reaction to {message_ts} message...')
    url = f'https://slack.com/api/reactions.add?token={get_token()}&channel={get_channel()}&name={reaction}&timestamp={message_ts}&pretty=1'
    response = requests.post(url)
    write_log('Success' if response.json()['ok'] else 'Fail', is_new_line=False)
    return response.json()['ok']


def get_reactions(message_ts):
    write_log(f'Getting reactions for {message_ts}...')
    url = f'https://slack.com/api/reactions.get?token={get_token()}&channel={get_channel()}&timestamp={message_ts}&pretty=1'
    response = requests.post(url)
    try:
        write_log('Success' if response.json()['message']['reactions'] else 'Fail', is_new_line=False)
        return response.json()['message']['reactions']
    except KeyError:
        return []


def remove_reaction(message_ts, reaction):
    write_log(f'Remove {reaction} reaction for {message_ts}...')
    url = f'https://slack.com/api/reactions.remove?token={get_token()}&name={reaction}&channel={get_channel()}&timestamp={message_ts}&pretty=1'
    response = requests.post(url)
    write_log('Success' if response.json()['ok'] else 'Fail', is_new_line=False)
    return response.json()['ok']


def change_reaction(message_ts, reaction):
    bot_id = get_bot_id()
    for current_reaction in get_reactions(message_ts):
        if bot_id in current_reaction['users']:
            remove_reaction(message_ts, current_reaction['name'])
    return add_reaction(message_ts, reaction)
