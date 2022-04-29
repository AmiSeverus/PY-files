import requests
import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from pprint import pprint
import vk
import db
import consts
from model import models


class ChatBot():

    def __init__(self):
        self.token = input('Token: ')
        self.vk_api = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_api)
        self.current_step = 0
        self.conn = db.DB().getConn()
        self.vk = vk.VK(self.token)
        self.missing_attr = ''
        self.message = ''
        self.user_id = ''
        self.search_attr = {}

    def get_black_list(self):
        return self.conn.query(
            models.matches_shown.pair_id
        ).filter_by(
            user_id=self.user_id
        ).all()

    def write_msg(self, user_id, message):
        self.vk_api.method(
            'messages.send',
            {
                'user_id': user_id,
                'message': message,
                'random_id': randrange(10 ** 7),
            }
        )

    def check_search_attr(self):
        self.missing_attr = ''
        for key, value in self.search_attr.items():
            if value is False:
                self.missing_attr = key
                return

    def isint(self, s):
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
        self.search_attr['age_to'] = self.search_attr['age']
        self.search_attr['age_from'] = self.search_attr['age']
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

    def process_search(self, event_user_id):
        matches_shown = self.get_black_list()
        black_list = []
        if matches_shown:
            for match in matches_shown:
                black_list.append(match[0])
        res = self.vk.search_pairs(self.search_attr, black_list)
        search_result_record = models.search_results()
        search_result_record.user_id = self.user_id
        search_result_record.search_attr = json.dumps(self.search_attr)
        if res['error_message'] or not res['results']:
            self.write_msg(event_user_id, consts.error_messages['404_pair'])
        else:
            res = res['results']
            search_result_record.search_results = json.dumps(res)
            if len(res) < 3:
                self.message = 'Найдены менее 3 совпадений'
            else:
                self.message = 'Из найденных совпадений приведены первые 3. Чтоб получить другие совпадения, повтори поиск.'
            self.write_msg(event_user_id, self.message)
            black_list = []
            cnt = 1
            for pair in res:
                full_name = pair['pair_fullname']
                link = 'https://vk.com/id' + str(pair['pair_id'])
                black_list.append(
                    {
                        'user_id': self.user_id,
                        'pair_id': pair['pair_id']
                    }
                )
                self.message = f'Совпадение {cnt}: зовут - {full_name}, ссылка - {link}'
                self.write_msg(event_user_id, self.message)
                if not pair['photos']:
                    self.message = 'Фото нет'
                    self.write_msg(event_user_id, self.message)
                else:
                    self.message = 'Топ-фото (не больше 3):'
                    self.write_msg(event_user_id, self.message)
                    for photo in pair['photos']:
                        self.write_msg(
                            event_user_id,
                            photo['sizes'][-1]['url']
                        )
                self.conn.add(
                    models.matches_shown(
                        user_id=self.user_id,
                        pair_id=pair['pair_id']
                    )
                )
                cnt += 1
        self.conn.add(search_result_record)
        self.conn.commit()
        self.write_msg(event_user_id, consts.error_messages['200'])
        self.write_msg(event_user_id, 'пока((')
        self.reset_state()

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
                            self.current_step = 1
                            self.message = 'Для себя?'
                            self.write_msg(event.user_id, self.message)
                        elif reply == 'нет':
                            self.write_msg(event.user_id, 'пока((')
                            self.reset_state()
                        else:
                            self.write_msg(
                                event.user_id,
                                consts.error_messages['400']
                            )
                            self.write_msg(event.user_id, self.message)
                elif self.current_step == 1:
                    if self.message == 'Для себя?':
                        if reply == 'да':
                            res = self.vk.get_search_attr(event.user_id)
                            if res['error_message']:
                                self.write_msg(
                                    event.user_id,
                                    consts.error_messages['404_user']
                                )
                                self.write_msg(
                                    event.user_id,
                                    consts.error_messages['200']
                                )
                                self.write_msg(event.user_id, 'пока((')
                                self.reset_state()
                            else:
                                self.user_id = res['results']['user_id']
                                self.search_attr = res['results']['search_attr']
                                self.current_step = 2
                                self.check_search_attr()
                                if not self.missing_attr:
                                    self.prepare_search_attr()
                                    self.process_search(event.user_id)
                                else:
                                    self.write_msg(
                                        event.user_id,
                                        consts.error_messages['206']
                                    )
                                    self.message = f'Введите {consts.attr_translation[self.missing_attr]}'
                                    if self.missing_attr == 'age':
                                        self.message += ' от 1 до 100 (включительно)'
                                    self.write_msg(event.user_id, self.message)
                                    if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                        self.write_msg(
                                            event.user_id,
                                            'Выберите цифру из предложенных ниже:'
                                        )
                                        self.write_msg(
                                            event.user_id,
                                            self.return_sub_str()
                                        )
                        elif reply == 'нет':
                            self.message = "Введите id или screen_name для кого найти пару"
                            self.write_msg(event.user_id, self.message)
                        else:
                            self.write_msg(
                                event.user_id,
                                consts.error_messages['400']
                            )
                            self.write_msg(event.user_id, self.message)
                    elif self.message == "Введите id или screen_name для кого найти пару":
                        if not reply:
                            self.write_msg(
                                event.user_id,
                                consts.error_messages['400']
                            )
                            self.write_msg(event.user_id, self.message)
                        else:
                            res = self.vk.get_search_attr(reply)
                            if res['error_message']:
                                self.write_msg(
                                    event.user_id,
                                    consts.error_messages['404_user']
                                )
                                self.write_msg(
                                    event.user_id,
                                    consts.error_messages['200']
                                )
                                self.write_msg(event.user_id, 'пока((')
                                self.reset_state()
                            else:
                                self.user_id = res['results']['user_id']
                                self.search_attr = res['results']['search_attr']
                                self.current_step = 2
                                self.check_search_attr()
                                if not self.missing_attr:
                                    self.prepare_search_attr()
                                    self.process_search(event.user_id)
                                else:
                                    self.write_msg(
                                        event.user_id,
                                        consts.error_messages['206']
                                    )
                                    self.message = f'Введите {consts.attr_translation[self.missing_attr]}'
                                    if self.missing_attr == 'age':
                                        self.message += ' от 1 до 100 (включительно)'
                                    self.write_msg(event.user_id, self.message)
                                    if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                        self.write_msg(
                                            event.user_id,
                                            'Выберите цифру из предложенных ниже:'
                                        )
                                        self.write_msg(
                                            event.user_id,
                                            self.return_sub_str()
                                        )
                    else:
                        self.write_msg(
                            event.user_id,
                            consts.error_messages['500']
                        )
                        self.write_msg(event.user_id, 'пока((')
                        self.reset_state()
                elif self.current_step == 2:
                    if not self.missing_attr:
                        self.write_msg(
                            event.user_id,
                            consts.error_messages['500']
                        )
                        self.write_msg(event.user_id, 'пока((')
                        self.reset_state()
                    else:
                        if not reply:
                            self.write_msg(
                                event.user_id,
                                consts.error_messages['400']
                            )
                            self.write_msg(event.user_id, self.message)
                            if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                self.write_msg(
                                    event.user_id,
                                    'Выберите цифру из предложенных ниже:'
                                )
                                self.write_msg(
                                    event.user_id,
                                    self.return_sub_str()
                                )
                        else:
                            if not self.check_attr(reply):
                                self.write_msg(
                                    event.user_id,
                                    consts.error_messages['400']
                                )
                                self.write_msg(event.user_id, self.message)
                                if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                    self.write_msg(
                                        event.user_id,
                                        'Выберите цифру из предложенных ниже:'
                                    )
                                    self.write_msg(
                                        event.user_id,
                                        self.return_sub_str()
                                    )
                            else:
                                if self.missing_attr != 'hometown':
                                    reply = int(reply)
                                self.search_attr[self.missing_attr] = reply
                                self.check_search_attr()
                                if not self.missing_attr:
                                    self.prepare_search_attr()
                                    self.process_search(event.user_id)
                                else:
                                    self.message = f'Введите {consts.attr_translation[self.missing_attr]}'
                                    if self.missing_attr == 'age':
                                        self.message += ' от 1 до 100 (включительно)'
                                    self.write_msg(event.user_id, self.message)
                                    if self.missing_attr == 'sex' or self.missing_attr == 'status':
                                        self.write_msg(
                                            event.user_id,
                                            'Выберите цифру из предложенных ниже:'
                                        )
                                        self.write_msg(
                                            event.user_id,
                                            self.return_sub_str()
                                        )
                else:
                    self.write_msg(event.user_id, consts.error_messages['500'])
                    self.write_msg(event.user_id, 'пока((')
                    self.reset_state()

if __name__ == "__main__":

    bot = ChatBot()
    bot.execute()
