class Ticket:
    id = None
    ticket_id = None
    subject = None
    topic = None
    department = None
    reporter = None
    ib_name = None
    brands = None
    assignee_name = None
    assignee_id = None
    status = None
    link = None
    last_activity = None
    last_message = None

    def __init__(self, ticket_dict=None):
        if ticket_dict:
            for attribute in ticket_dict.keys():
                setattr(self, attribute, ticket_dict[attribute])

    def __gt__(self, other):
        return self.last_activity > other.last_activity

    def __lt__(self, other):
        return self.last_activity < other.last_activity


