import time


def how_much_time_passed(timestamp):
    time_passed = {}
    timestamp_difference = int(time.time()) - int(timestamp)
    days = timestamp_difference // 86400
    hours = (timestamp_difference % 86400) // 3600
    minutes = (timestamp_difference % 3600) // 60
    seconds = (timestamp_difference % 60)
    if days:
        time_passed['days'] = days
        time_passed['hours'] = hours
    elif hours:
        time_passed['hours'] = hours
        time_passed['minutes'] = minutes
    elif minutes:
        time_passed['minutes'] = minutes
        time_passed['seconds'] = seconds
    else:
        time_passed['seconds'] = seconds
    return time_passed
