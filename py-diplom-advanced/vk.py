from pprint import pprint
import requests
from sqlalchemy import false, values

import calendar
import datetime
from dateutil.relativedelta import *


# vk_token = 'e9d323112cddc1440cd28b722a5215b7fdbfa263e8c6a3120e2ca78207c249b93a9424b752e9aeaca10a9' 
# - standalone

vk_token = 'cce07f199ea32d10e6cd991f5e6291bcae8f4f1e82e95abf7442d14e3ddc8e08c7f2fbc34c21f37458973'
# py-test

class VK:

    def __init__(self, token):
        self.vk_url = 'https://api.vk.com/method/'
        self.params = '?access_token=' + token + '&v=5.131&album_id=profile&extended=1'
        self.error_message = ''
        self.results = []
        self.search_attr = {'sex':False, 'hometown':False, 'status':False, 'age':False}
        self.user_id = ''


    def get_user(self, q):
        res = requests.get(self.vk_url + 'users.get' + self.params + '&fields=bdate,sex,home_town,relation&user_ids=' + str(q)).json()['response']
        self.error_message = ''
        self.results = []
        if len(res) < 1:
            self.error_message = 'Пользователь не найден'
        else:
            print(res[0])
            self.fill_in_search_attr(res[0])


    def fill_in_search_attr(self, user):
        for key, value in user.items():
            if key == 'bdate':
                self.process_date(value)
            # if key == 'sex':
                # self.search_attr['sex'] = value
            if key == 'home_towm' and value:
                self.search_attr['hometown'] = value
            if key == 'relation' and value:
                self.search_attr['status'] = value
            if key == 'id':
                self.user_id = value


    def process_date(self, date):
        date_arr = date.split()
        if len(date_arr) != 3:
            return
        date_b = datetime.date(year=date_arr[2], month=date_arr[1], day=date_arr[0])
        date_today = datetime.date.today()
        age = relativedelta(date_today, date_b)
        if age > 0:
            self.search_attr['age'] = age


    def get_search_attr(self,q):
        self.error_message = ''
        self.search_attr = {'sex':False, 'hometown':False, 'status':False, 'age':False}
        self.user_id = ''
        self.get_user(q)
        return {'error_message':self.error_message, 'results':{'search_attr': self.search_attr, 'user_id': self.user_id}}

    # конец первого шага

    def search_users(self, search_attr):
        self.search_attr = search_attr
        pass


    def get_user_photo_from_VK(self, user_id):
        res = requests.get(self.vk_url + 'photos.get' + self.params + '&owner_id=' + str(user_id)).json()
        return res
        # if 'error' in res:
        #     return {'status': 'error', 'message': 'Слишком много запросов'}
        # else:
        #     pprint(res)
            # response = res['response']
            # photos_count = response['count']
            # if photos_count < 1:
            #     return {'status': 'error', 'message': 'Нет фотографий'}
            # if self.cnt < 1:
            #     self.cnt = 5
            # if self.cnt > photos_count:
            #     self.cnt = photos_count
            # photos_info = response['items']
            # cnt = self.cnt
            # while cnt != 0:
            #     cnt = cnt-1
            #     photo_sizes = photos_info[cnt]['sizes']
            #     for size in self.photo_sizes_sort_desc:
            #         added = False
            #         for photo_size in photo_sizes:
            #             if photo_size['type'] == size:
            #                 added = True
            #                 self.max_photos.append({
            #                     'id': photos_info[cnt]['id'],
            #                     'url': photo_size['url'],
            #                     'likes': photos_info[cnt]['likes']['count'],
            #                     'size': photo_size['type']
            #                 })
            #                 break
            #         if added:
            #             break
        # return {'status': 'success'}

# vk_chat = VK(vk_token)

# pprint(vk_chat.get_user('natalia_tataur'))
