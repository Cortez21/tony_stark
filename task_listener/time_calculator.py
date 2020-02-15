import time
from task_listener.log_writer import write as write_log


def how_much_time_passed(timestamp):
    write_log('Starting calculating how much time passed...')
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
    write_log('Time calculating is done. Result is {}'.format(time_passed))
    return time_passed
