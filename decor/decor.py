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

def parametrized_decor(parameter):
    def log_decorator(fn):
        def new_fn(*args, **kwars):
            datetime_stamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            res = fn(*args, **kwars)
            with open(os.path.join(parameter, 'result.txt'), 'a', encoding='utf-8') as result:
                result.write(f'Дата и время вызова: {datetime_stamp}\nИмя функции: {fn.__name__}\nАргументы: {args}, {kwars}\nВозвращаемое значение:{res}\nПуть к логгеру:{parameter}\n\n')
            return res
        return new_fn
    return log_decorator