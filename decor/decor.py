import os
import datetime


def log_decorator(fn):

    def logger(*args, **kwargs):
        res = fn(*args, **kwargs)
        datetime_stamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open('result.txt', 'a', encoding='utf-8') as result:
            result.write(f'Дата и время вызова: {datetime_stamp}\nИмя функции: {fn.__name__}\nАргументы: {args}, {kwargs}\nВозвращаемое значение:{res}\nПуть к логгеру:{os.path.abspath("result.txt")}\n\n')
        return

    return logger