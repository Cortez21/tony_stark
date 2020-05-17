import json

PATH_TO_CONFIG = 'task_listener/config.json'


def read_config():
    with open(PATH_TO_CONFIG, 'r') as conf_file:
        conf_dict = json.load(conf_file)
        return conf_dict


def get_psql_credentials():
    return read_config()['psql']


def get_ts_cookies():
    return read_config()['ticket_system']['cookies']


def get_slack_token():
    return read_config()['slack']['token']


def get_slack_channel():
    return read_config()['slack']['channel']


def get_department_icon(department):
    return read_config()['slack']['department_icons'][department]


def get_default_assignee():
    return read_config()['slack']['if_absent_assignee_sent_to']


def get_bot_id():
    return read_config()['slack']['bot_id']


def get_reaction(status):
    return read_config()['slack']['reactions'][status]
