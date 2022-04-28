from email import message
import requests
import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange

import vk
import db
import consts
from pprint import pprint

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
        self.token = input('Token: ')
        self.vk_api = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_api)
        self.steps = [{'step_name':'init', 'step_status':False}, {'step_name':'user', 'step_status':False}, {'step_name':'user_det', 'step_status':False}, {'step_name':'search_attr', 'step_status':False},{'step_name':'end_search', 'step_status':False}]
        self.current_step = 0
        self.conn = db.DB().getConn()
        self.vk = vk.VK(self.token)
        self.missing_attr = ''
        self.message = ''
        self.user_id = ''
        self.search_attr = []


    def write_msg(self, user_id, message):
        self.vk_api.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),})


    def check_search_attr(self):
        self.missing_attr = ''
        for key, value in self.search_attr.items():
            if isinstance(value, bool) and value == False:
                self.missing_attr = key
                return

    def isint(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False    

    def check_attr(self, value):
        check_pass = True
        if self.missing_attr != 'hometown':
            if not self.isint(value):
                check_pass = False
            else:
                value = int(value)
                if self.missing_attr == 'age' and (value < 1 or value > 100):
                    check_pass = False
                if self.missing_attr == 'status' and (value < 0 or value >= len(consts.status_attr)):
                    check_pass = False
                if self.missing_attr == 'sex' and (value < 0 or value >= len(consts.sex_attr)):
                    check_pass = False
        return check_pass 


    def prepare_search_attr(self):
        self.search_attr['age_to'] = self.search_attr['age_from'] = self.search_attr['age']
        del self.search_attr['age']
        if not self.search_attr['status']:
            del self.search_attr['status']
        if not self.search_attr['sex']:
            del self.search_attr['sex']


    def return_sub_str(self):
        if self.missing_attr == 'sex':
            return (", ".join(list(consts.sex_attr)))
        elif self.missing_attr == 'status':
            return (", ".join(list(consts.status_attr)))


    def reset_state(self):
        self.current_step = 0
        self.missing_attr = ''
        self.message = ''
        self.user_id = ''
        for step in self.steps:
            step['step_status'] = False
        

    def execute(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply = event.text.lower().strip()
                if reply == 'выход':
                    self.write_msg(event.user_id, 'пока((')
                    self.reset_state()
                elif self.current_step == 0:
                    if not self.message:
                        self.message = "Привет, найти пару?"
                        self.write_msg(event.user_id, self.message)
                    else:
                        if reply == 'да':
                            self.steps[self.current_step]['step_status'] = True
                            self.current_step = 1
                            self.message = 'Для себя?'
                            self.write_msg(event.user_id, self.message)
                        elif reply == 'нет':
                            self.write_msg(event.user_id, 'пока((')
                            self.reset_state()
                        else:
                            self.write_msg(event.user_id, consts.error_messages['400'])
                            self.write_msg(event.user_id, self.message)
                elif self.current_step == 1:
                    if self.message == 'Для себя?':
                        if reply == 'да':
                            res = self.vk.get_search_attr(event.user_id)
                            if res['error_message']:
                                self.write_msg(event.user_id, consts.error_messages['404_user'])
                                self.write_msg(event.user_id, 'пока((')
                                self.reset_state()
                            else:
                                self.user_id = res['results']['user_id']
                                self.search_attr = res['results']['search_attr']
                                self.steps[self.current_step]['step_status'] = True
                                self.current_step = 2
                                self.check_search_attr()
                                if not self.missing_attr:
                                    self.steps[self.current_step]['step_status'] = True
                                    self.current_step = 3
                                else:
                                    self.write_msg(event.user_id, consts.error_messages['206'])
                                    self.message = f'Введите {consts.attr_translation[self.missing_attr]}'
                                    if self.missing_attr == 'age':
                                        self.message += ' от 1 до 100 (включительно)'
                                    self.write_msg(event.user_id, self.message)
                                    if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                        self.write_msg(event.user_id, 'Выберите цифру из предложенных ниже:')
                                        self.write_msg(event.user_id, self.return_sub_str())
                        elif reply == 'нет':
                            self.message = "Введите id или screen_name для кого найти пару"
                            self.write_msg(event.user_id, self.message)
                        else:
                            self.write_msg(event.user_id, consts.error_messages['400'])
                            self.write_msg(event.user_id, self.message)
                    elif self.message == "Введите id или screen_name для кого найти пару":
                        if not reply:
                            self.write_msg(event.user_id, consts.error_messages['400'])
                            self.write_msg(event.user_id, self.message)
                        else:
                            res = self.vk.get_search_attr(reply)
                            if res['error_message']:
                                self.write_msg(event.user_id, consts.error_messages['404_user'])
                                self.write_msg(event.user_id, 'пока((')
                                self.reset_state()
                            else:                         
                                self.user_id = res['results']['user_id']
                                self.search_attr = res['results']['search_attr']
                                self.steps[self.current_step]['step_status'] = True
                                self.current_step = 2
                                self.check_search_attr()
                                if not self.missing_attr:
                                    self.steps[self.current_step]['step_status'] = True
                                    self.current_step = 3
                                    self.prepare_search_attr()
                                else:
                                    self.write_msg(event.user_id, consts.error_messages['206'])
                                    self.message = f'Введите {consts.attr_translation[self.missing_attr]}'
                                    if self.missing_attr == 'age':
                                        self.message += ' от 1 до 100 (включительно)'                                    
                                    self.write_msg(event.user_id, self.message)
                                    if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                        self.write_msg(event.user_id, 'Выберите цифру из предложенных ниже:')
                                        self.write_msg(event.user_id, self.return_sub_str())
                    else:
                        self.write_msg(event.user_id, consts.error_messages['500'])
                        self.write_msg(event.user_id, 'пока((')
                        self.reset_state()
                elif self.current_step == 2:
                    if not self.missing_attr:
                        self.write_msg(event.user_id, consts.error_messages['500'])
                        self.write_msg(event.user_id, 'пока((')
                        self.reset_state()
                    else:
                        if not reply:
                            self.write_msg(event.user_id, consts.error_messages['400'])
                            self.write_msg(event.user_id, self.message)
                            if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                self.write_msg(event.user_id, 'Выберите цифру из предложенных ниже:')
                                self.write_msg(event.user_id, self.return_sub_str())
                        else:
                            if not self.check_attr(reply):
                                self.write_msg(event.user_id, consts.error_messages['400'])
                                self.write_msg(event.user_id, self.message)
                                if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                    self.write_msg(event.user_id, 'Выберите цифру из предложенных ниже:')
                                    self.write_msg(event.user_id, self.return_sub_str())
                            else:
                                if self.missing_attr != 'hometown':
                                    reply = int(reply)
                                self.search_attr[self.missing_attr] = reply
                                self.check_search_attr()
                                if not self.missing_attr:
                                    self.steps[self.current_step]['step_status'] = True
                                    self.current_step = 3
                                    self.prepare_search_attr()
                                else:
                                    self.message = f'Введите {consts.attr_translation[self.missing_attr]}'
                                    if self.missing_attr == 'age':
                                        self.message += ' от 1 до 100 (включительно)'
                                    self.write_msg(event.user_id, self.message)
                                    if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                        self.write_msg(event.user_id, 'Выберите цифру из предложенных ниже:')
                                        self.write_msg(event.user_id, self.return_sub_str())                              
                elif self.current_step == 3:
                    self.write_msg(event.user_id, 'В разработке')

bot = ChatBot()

bot.execute()