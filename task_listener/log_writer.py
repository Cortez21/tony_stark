import datetime


def write(text, is_new_line=True):
    if not check_if_exist():
        create_log_file()
    date = datetime.datetime.now()
    fo = open('task_listener/logs/{}.log'.format(date.date()), 'a')
    fo.write('{}{}{}'.format('\n' if is_new_line else '', f"[{date.time()}]: " if is_new_line else '', text))


def create_log_file(date=datetime.date.fromisoformat('2020-01-01').today()):
    fo = open('task_listener/logs/{}.log'.format(date), 'w')
    fo.close()


def check_if_exist():
    exist = True
    try:
        f = open('task_listener/logs/{}.log'.format(datetime.datetime.now().date()))
    except IOError:
        exist = False
    return exist


if __name__ == '__main__':
    write('test')