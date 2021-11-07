from pprint import pprint

from datetime import datetime as dt
from datetime import timedelta
import requests

# Задача 1

class SuperHero:
    def __init__(self, name):
        res = requests.get(url='https://superheroapi.com/api/2619421814940190/search/' + name.lower()).json()['results']
        if len(res) == 0:
            # print('Нет такого персонажа')
            self.name = 'Нет такого персонажа'
            self.intelligence = 0
        elif len(res) == 1:
            # print(res[0]['name'])
            self.name = res[0]['name']
            self.intelligence = int(res[0]['powerstats']['intelligence'])
        else:
            for pers in res:
                # print(pers['name'])
                if pers['name'].lower() == name.lower():
                    # print(name)
                    self.name = pers['name']
                    self.intelligence = int(pers['powerstats']['intelligence'])

hulk = SuperHero('Hulk')
capitan_america = SuperHero('Captain America')
thanos = SuperHero('Thanos')

def smartest (list):
    smartest_pers = 'Никого нет'
    intelligence = 0
    for pers in list:
        if pers.intelligence > intelligence:
            smartest_pers = pers
            intelligence = pers.intelligence
    return smartest_pers

print(smartest([hulk, capitan_america, thanos]).name)

# Задача 2

class YaUploader:
    def __init__(self):
        self.token = input('Введите токен: ')
        self.url = 'https://cloud-api.yandex.net:443'
    
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_upload_link (self, disk_path):
        params = {'path': disk_path.lower()}
        return requests.get(url=self.url + '/v1/disk/resources/upload', params = params,  headers=self.get_headers()).json()['href']

    def upload_file(self, disk_path, filename):
        response = requests.put(self.get_upload_link(disk_path), data=open(filename, 'rb'))
        return(response.status_code)

ya = YaUploader()

print(ya.upload_file('/test/test.txt', 'test.txt'))

# Задача 3

def get_topics_by_tag_and_day(tag,days_minus=2):
    url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow'
    ts = int(dt.timestamp(dt.now()-timedelta(days=days_minus)))
    url += f'&fromdate={ts}&tagged={tag}'
    res = requests.get(url)
    if requests.status == 200:
        return res.json()['item']
    else:
        return 'Что-то пошло не так'
    
get_topics_by_tag_and_day('python', 2)