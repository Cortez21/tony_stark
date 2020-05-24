import json
import os

PATH_TO_CONFIG = 'task_listener/config.json'


def read_config():
    with open(PATH_TO_CONFIG, 'r') as conf_file:
        conf_dict = json.load(conf_file)
        return conf_dict


def get_psql_credentials():
    psql_creds_dict = dict()
    psql_creds_dict['user'] = os.environ['PSQL_USER']
    psql_creds_dict['password'] = os.environ['PSQL_PASSWORD']
    psql_creds_dict['host'] = os.environ['PSQL_HOST']
    psql_creds_dict['port'] = os.environ['PSQL_PORT']
    return psql_creds_dict


def get_ts_cookies():
    return os.environ['TICKET_SYSTEM_COOKIES']


def get_slack_token():
    return os.environ['SLACK_TOKEN']


def get_slack_channel():
    return os.environ['SLACK_CHANNEL']


def get_department_icon(department):
    return read_config()['slack']['department_icons'][department]


def get_default_assignee():
    return read_config()['slack']['if_absent_assignee_sent_to']


def get_bot_id():
    return os.environ['SLACK_BOT_ID']


def get_reaction(status):
    return read_config()['slack']['reactions'][status]
