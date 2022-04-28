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
        # self.params = '?access_token=' + token + '&v=5.131'
        self.params = '?access_token=' + 'e9d323112cddc1440cd28b722a5215b7fdbfa263e8c6a3120e2ca78207c249b93a9424b752e9aeaca10a9' + '&v=5.131'
        self.error_message = ''
        self.results = []
        self.search_attr = {'sex':False, 'hometown':False, 'status':False, 'age':False}
        self.user_id = ''
        self.black_list = []


    def get_user(self, q):
        res = requests.get(self.vk_url + 'users.get' + self.params + '&fields=bdate,sex,home_town,relation&user_ids=' + str(q)).json()
        self.error_message = ''
        if 'error' in res:
            self.error_message = res['error']['error_msg']
        else:
            res = res['response']
            if len(res) < 1:
                self.error_message = 'Пользователь не найден'
            else:
                self.fill_in_search_attr(res[0])


    def fill_in_search_attr(self, user):
        for key, value in user.items():
            if key == 'bdate':
                self.process_date(value)
            if key == 'sex':
                self.search_attr['sex'] = value
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


    def search_users(self):

        self.error_message = ''
        cnt = 0;
        params = ''
        for attr_name, attr_value in self.search_attr.items():
            params += '&' + attr_name + '=' + str(attr_value)

        offset = cnt * 20

        if offset:
            params += '&offset = ' + str(offset)

        while len(self.results) < 3:
            res = requests.get(self.vk_url + 'users.search' + self.params + params).json()
            if 'error' in res:
                self.error_message = res['error']['error_msg']
                break
            else:
                res = res['response']['items']
                if len(res) < 1:
                    if (len(self.results) < 1):
                        self.error_message = 'Пользователь не найден'
                    break
                else:
                    for item in res:
                        if item['id'] not in self.black_list and not item['is_closed']:
                            self.results.append({'pair_id':item['id'] })
                        if len(self.results) >= 3:
                            break


    def get_photos(self, user_id):
        res = requests.get(self.vk_url + 'photos.get' + self.params + '&album_id=profile&extended=1&photo_sizes=1&owner_id=' + str(user_id)).json()
        if 'error' in res:
            return []
        else:
            res = res['response']['items']
            if len(res) < 1:
                return []
            elif len(res) <= 3:
                return res
            else:
                return self.select_top3_photos(res)


    def select_top3_photos(self,photos):
        res = {'top1':'', 'top2':'', 'top3':''}
        cnt = 0
        for photo in photos:
            if cnt == 0:
                res['top1'] = photo
            elif cnt == 1:
                if res['top1']['likes']['count'] > photo['likes']['count']:
                    res['top2'] = photo
                else:
                    res['top2'] = res['top2']
                    res['top2'] = photo
            elif cnt == 2:
                if res['top2']['likes']['count'] > photo['likes']['count']:
                    res['top3'] = photo
                else:
                    if res['top1']['likes']['count'] > photo['likes']['count']:
                        res['top3'] = res['top2']
                        res['top2'] = photo
                    else:
                        res['top3'] = res['top2']
                        res['top2'] = res['top1']
                        res['top1'] = photo
            else:
                res = self.check_res(res, photo)
            cnt += 1
        return res


    def check_res(self, res, photo):
        if photo['likes']['count'] <= res['top3']['likes']['count']:
            return res
        elif photo['likes']['count'] <= res['top2']['likes']['count']:
            res['top3'] = photo
            return res
        elif photo['likes']['count'] <= res['top1']['likes']['count']:
            res['top3'] = res['top2']
            res['top2'] = photo
            return res
        else:
            res['top3'] = res['top2']
            res['top2'] = res['top1']
            res['top1'] = photo
            return res            


    def search_pairs(self, search_attr, black_list=[]):
        self.search_attr = search_attr
        self.black_list = black_list
        self.results = []
        self.error_message = ''
        self.search_users()
        if len(self.results) > 0:
            for pair in self.results:
                pair['photos'] = self.get_photos(pair['pair_id'])
        return {'error_message':self.error_message, 'results':self.results}

    # конец второго шага
