from task_listener import parser, slack, data_keeper, time_calculator, message_formatter, connector


def check_if_exist(parsed_tickets_data, checking_ticket_id):
    result = False
    for ticket_data in parsed_tickets_data:
        if checking_ticket_id in ticket_data['ticket_id']:
            result = True
            break
    return result


def main():
    fresh_tickets_data = connector.get_inbox_data()
    parsed_tickets_data = parser.get_tickets_from_inbox_data(fresh_tickets_data)
    for ticket_data in parsed_tickets_data:
        ticket_id = ticket_data['ticket_id']
        if data_keeper.check_if_exist(ticket_id):
            if data_keeper.get_ticket_status(ticket_id) == 'closed':
                time_passed = time_calculator.how_much_time_passed(data_keeper.get_ticket_timestamp(ticket_id))
                data_keeper.update_ticket_status(ticket_id, 'open')
                slack.send_message_to_me(message_formatter.create_for_exist(ticket_data, time_passed))
        else:
            data_keeper.insert_ticket(ticket_id)
            slack.send_message_to_me(message_formatter.create_for_new(ticket_data))
    loaded_opened_tickets = data_keeper.get_opened_tickets()
    for opened_ticket_id in loaded_opened_tickets:
        if not check_if_exist(parsed_tickets_data, opened_ticket_id):
            data_keeper.update_ticket_status(opened_ticket_id, 'closed')


if __name__ == '__main__':
    main()
