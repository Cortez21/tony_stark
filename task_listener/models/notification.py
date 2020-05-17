class Notification:
    id = None
    ticket_id = None
    initial = None
    team_id = None
    channel = None
    slack_ts = None

    def __init__(self, ticket_dict):
        for attribute in ticket_dict.keys():
            setattr(self, attribute, ticket_dict[attribute])