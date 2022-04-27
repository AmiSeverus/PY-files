from email import message
import requests
import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange

import vk
import db

# token = input('Token: ')

# token = 'cce07f199ea32d10e6cd991f5e6291bcae8f4f1e82e95abf7442d14e3ddc8e08c7f2fbc34c21f37458973'

# vk_token = 'e9d323112cddc1440cd28b722a5215b7fdbfa263e8c6a3120e2ca78207c249b93a9424b752e9aeaca10a9'

# vk = vk_api.VkApi(token=token)
# longpoll = VkLongPoll(vk)
# start_search_flag = False
# search_attr = {'возраст':'', 'пол':'', 'город':'', 'семейное положение':'',}
# message = ''


# def start_search(flag):
#     start_search_flag = flag

# def clear_search_attr():
#     for attr in search_attr:
#         attr = ''

# def set_search_attr(attr_name, value):
#     if attr_name in search_attr:
#         search_attr[attr_name] = value

# def set_message(text):
#     message = text

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#         if event.to_me:
#             if event.text == "привет":
#                 # write_msg(event.user_id, f"Хай, {event.user_id}")
#                 write_msg(event.user_id, "https://vk.com/id33718573?z=photo33718573_413817792%2Falbum33718573_0%2Frev")
#             elif event.text == "пока":
#                 write_msg(event.user_id, "Пока((")
#             else:
#                 write_msg(event.user_id, "Не поняла вашего ответа...")


class ChatBot():

    def __init__(self):
        self.vk_api = vk_api.VkApi(token=input('Token: '))
        self.longpoll = VkLongPoll(self.vk_api)
        self.steps = [{'init':False}, {'user':False}, {'user_det':False}, {'search_attr':False},{'end_search':False}]
        self.current_step = 0
        self.conn = db.DB().getConn()
        self.vk = vk.VK()
        self.missed_attr = ''
        self.sex_attr = ['0 - любой', '1 - женщина', '2 - мужчина']
        self.status_attr = ['0 - любой', 
                            '1 - не женат (не замужем)', 
                            '2 - встречается', 
                            '3 - помолвлен(-а)', 
                            '4 - женат (замужем)', 
                            '5 — всё сложно', 
                            '6 — в активном поиске',
                            '7 — влюблен(-а)',
                            '8 — в гражданском браке']
        self.message = ''


    def write_msg(self, user_id, message):
        self.vk_api.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


    def request_attr(self, attr_name, attr_value):
        pass


    def execute(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'выход':
                    self.current_step = 0
                    self.message = ''
                    for key, value in self.steps.item():
                        if key > 0 and key < 4:
                            for val in value:
                                val = False
                if self.current.step == 0:
                    if not self.message:
                        self.message = "Привет, найти пару?"
                        self.write_msg(event.user_id, self.message)
                    else:
                        reply = event.text.lower().trim()
                        if reply == 'да':
                            for value in self.steps[self.current_step]:
                                value = True
                            self.current_step = 1
                            self.message = 'Для себя?'
                            self.write_msg(event.user_id, "Привет, найти пару?")
                # if event.text == "привет":
                #     # write_msg(event.user_id, f"Хай, {event.user_id}")
                #     self.write_msg(event.user_id, "Привет")
                # elif event.text == "пока":
                #     self.write_msg(event.user_id, "Пока((")
                # else:
                #     self.write_msg(event.user_id, "Не поняла вашего ответа...")