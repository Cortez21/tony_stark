class Assignee:
    id = None
    assignee_name = None
    slack_id = None

    def __init__(self, attributes_dict):
        for attribute in attributes_dict.keys():
            setattr(self, attribute, attributes_dict[attribute])