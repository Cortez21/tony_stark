import csv
import time

_path_to_tickets_csv = 'task_listener/tickets.csv'


def get_cookies(path):
    fo = open(path, 'r')
    data = fo.read()
    return data


def check_if_exist(ticket_id):
    result = False
    with open(_path_to_tickets_csv, 'r') as csvfile:
        for ticket_data in csv.reader(csvfile, delimiter=","):
            if ticket_id in ticket_data:
                result = True
                break
    return result


def get_ticket_status(ticket_id):
    result = None
    with open(_path_to_tickets_csv, 'r') as csvfile:
        for ticket_data in csv.reader(csvfile, delimiter=","):
            if ticket_data and ticket_data[0] == ticket_id:
                result = ticket_data[1]
    return result


def get_ticket_timestamp(ticket_id):
    result = None
    with open(_path_to_tickets_csv, 'r') as csvfile:
        for ticket_data in csv.reader(csvfile, delimiter=","):
            if ticket_data and ticket_data[0] == ticket_id:
                result = ticket_data[2]
    return result


def load_all():
    tickets_dict = {}
    with open(_path_to_tickets_csv, 'r') as csvfile:
        for ticket in csv.reader(csvfile, delimiter=","):
            if ticket:
                tickets_dict[ticket[0]] = ticket
    return tickets_dict


def write_all(tickets_data_dict):
    with open(_path_to_tickets_csv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for ticket in tickets_data_dict.values():
            writer.writerow(ticket)


def insert_ticket(ticket_id):
    tickets_data_dict = load_all()
    tickets_data_dict[ticket_id] = [ticket_id, 'open', int(time.time())]
    write_all(tickets_data_dict)


def get_opened_tickets():
    opened_tickets_list = []
    loaded_tickets_data = load_all()
    for ticket in loaded_tickets_data:
        if 'open' in loaded_tickets_data[ticket]:
            opened_tickets_list.append(ticket)
    return opened_tickets_list


def update_ticket_status(ticket_id, ticket_status):
    loaded_tickets_data = load_all()
    loaded_tickets_data[ticket_id] = [ticket_id, ticket_status, int(time.time())]
    write_all(loaded_tickets_data)