from time import sleep

import requests

from task_listener.config_reader import get_slack_token as get_token, get_slack_channel as get_channel, get_bot_id


def send_message(message):
    url = f'https://slack.com/api/chat.postMessage?token={get_token()}&channel={get_channel()}&text={message}&pretty=1'
    response = requests.post(url)
    return response


def get_permalink(message_ts):
    url = f'https://slack.com/api/chat.getPermalink?token={get_token()}&channel={get_channel()}&message_ts={message_ts}&unfurl_links=true&pretty=1'
    response = requests.get(url)
    return response.json()['permalink']


def add_reaction(message_ts, reaction):
    url = f'https://slack.com/api/reactions.add?token={get_token()}&channel={get_channel()}&name={reaction}&timestamp={message_ts}&pretty=1'
    response = requests.post(url)
    return response.json()['ok']


def get_reactions(message_ts):
    url = f'https://slack.com/api/reactions.get?token={get_token()}&channel={get_channel()}&timestamp={message_ts}&pretty=1'
    response = requests.post(url)
    try:
        return response.json()['message']['reactions']
    except KeyError:
        return []


def remove_reaction(message_ts, reaction):
    url = f'https://slack.com/api/reactions.remove?token={get_token()}&name={reaction}&channel={get_channel()}&timestamp={message_ts}&pretty=1'
    response = requests.post(url)
    return response.json()['ok']


def change_reaction(message_ts, reaction):
    bot_id = get_bot_id()
    for current_reaction in get_reactions(message_ts):
        if bot_id in current_reaction['users']:
            remove_reaction(message_ts, current_reaction['name'])
    return add_reaction(message_ts, reaction)
