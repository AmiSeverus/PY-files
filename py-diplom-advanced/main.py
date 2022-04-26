import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange

token = input('Token: ')

# token = 'cce07f199ea32d10e6cd991f5e6291bcae8f4f1e82e95abf7442d14e3ddc8e08c7f2fbc34c21f37458973'

# vk_token = 'e9d323112cddc1440cd28b722a5215b7fdbfa263e8c6a3120e2ca78207c249b93a9424b752e9aeaca10a9'

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
start_search_flag = False
search_attr = {'возраст':'', 'пол':'', 'город':'', 'семейное положение':'',}
message = ''


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def start_search(flag):
    start_search_flag = flag

def clear_search_attr():
    for attr in search_attr:
        attr = ''

def set_search_attr(attr_name, value):
    if attr_name in search_attr:
        search_attr[attr_name] = value

def set_message(text):
    message = text

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.text == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif event.text == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")