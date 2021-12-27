from pprint import pprint
import requests
import time
import json


if __name__ == "__main__":

    class Get_max_photo_from_VK:
        def __init__(self):
            self.owners_id = set()
            self.vk_url = 'https://api.vk.com/method/'
            self.params = '?access_token=958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008&v=5.131&album_id=profile&extended=1'
            self.photo_sizes_sort_desc = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'm', 'o', 's']
            self.max_photos = []

        def set_ids(self):
            add = 'yes'
            error = " "
            while add.lower() == 'yes':
                search = input('Введите вид поиска (id / username / current - фото по текущему пользователю): ')
                if search == 'id':
                    self.owners_id.add(int(input('Введите id пользователя: ')))
                elif search == 'username':
                    username = input('Введите имя пользователя: ').strip()
                    if username:
                        res = self.get_user_id(username)
                        if res['status'] == 'success':
                            self.owners_id.add(int(res['id']))
                        else:
                            error = " не "
                            print(res['message'])
                    else:
                        error = " не "
                        print("Передана пустая строка")
                else:
                    print('Поиск по текущему пользователю')
                    self.owners_id.add('current')
                print('Id пользователя ' + error + 'добавлен')
                add = input('Добавить ещё пользователя (yes/no): ')

        def get_user_id(self, username):
            vk_search_url = self.vk_url + 'utils.resolveScreenName' + self.params + '&screen_name=' + username
            response = requests.get(url=vk_search_url)
            if response.status_code == 200 and 'response' in response.json() and 'type' in response.json()['response']:
                if response.json()['response']['type'] == 'user':
                    res = {'status': 'success', 'id': response.json()['response']['object_id']}
                else:
                    res = {'status': 'error', 'message': 'По данному username найден не пользователь, а ' + response.json()['response']['type']}
            else:
                res = {'status': 'error', 'message': 'Пользователь не найден'}
            return res

        def get_max_photo_url_from_VK(self, url):
            time.sleep(1)
            res = requests.get(url).json()
            if 'error' in res:
                return {'status': 'error', 'message': 'Слишком много запросов'}
            response = res['response']
            photos_count = response['count']
            if photos_count < 1:
                return {'status': 'error', 'message': 'Нет фотографий'}
            if self.cnt < 1:
                self.cnt = 5
            if self.cnt > photos_count:
                self.cnt = photos_count
            photos_info = response['items']
            cnt = self.cnt
            while cnt != 0:
                cnt = cnt-1
                photo_sizes = photos_info[cnt]['sizes']
                for size in self.photo_sizes_sort_desc:
                    added = False
                    for photo_size in photo_sizes:
                        if photo_size['type'] == size:
                            added = True
                            self.max_photos.append({
                                'id': photos_info[cnt]['id'],
                                'url': photo_size['url'],
                                'likes': photos_info[cnt]['likes']['count'],
                                'size': photo_size['type']
                            })
                            break
                    if added:
                        break
            return {'status': 'success'}

        def execute(self):
            self.set_ids()
            self.cnt = int(input('Введите количество фото для сохранения или цифру - 0, тогда сохранится 5 фото: '))
            vk_url = self.vk_url + 'photos.get' + self.params
            if len(self.owners_id) < 1:
                print('Пользователи не переданы')
                return
            for id in self.owners_id:
                if id == 'current':
                    res = self.get_max_photo_url_from_VK(vk_url)
                else:
                    res = self.get_max_photo_url_from_VK(vk_url + '&owner_id=' + str(id))
                if res['status'] == 'error':
                    print(res['message'])
                else:
                    print(f'Фото пользователя {id} найдено')

    class upload_to_Ya:
        def __init__(self):
            self.ya_url = 'https://cloud-api.yandex.net:443'

        def get_headers(self):
            return {
                'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)
            }

        def create_folder_Ya(self):
            if_exists = self.check_if_exists(self.ya_folder_path)
            if not if_exists:
                params = {'path': self.ya_folder_path}
                requests.put(url=self.ya_url + '/v1/disk/resources', params=params,  headers=self.get_headers())
                print('Папка создана')
            else:
                print('Папка уже существует')

        def check_if_exists(self, path):
            params = {'path': path}
            res = requests.get(url=self.ya_url + '/v1/disk/resources', params=params, headers=self.get_headers())
            if res.status_code == 200:
                return True
            else:
                return False

        def upload_files_Ya(self, photos):
            json_data = []
            json_done = 'не'
            for photo in photos:
                loaded = ' не'
                name = str(photo['likes']) + '.jpg'
                url = self.ya_folder_path + '/' + name
                is_exists = self.check_if_exists(url)
                if is_exists:
                    print("Файл под именем - " + name + ' уже существует. Добавлен id к имени')
                    name = str(photo['likes']) + '-' + str(photo['id']) + '.jpg'
                params = {'path': self.ya_folder_path + '/' + name, 'url': photo['url']}
                res = requests.post(url=self.ya_url + '/v1/disk/resources/upload', params=params, headers=self.get_headers())
                if res.status_code == 202:
                    json_data.append({'file_name': name, 'size': photo['size']})
                    loaded = " "
                print('Фото ' + photo['url'] + ' пользователя ' + str(photo['id']) + loaded + 'загружено')
                if res.status_code != 202:
                    print(res.json()['message'])
            if json_data:
                with open('./file.json', 'w') as json_file:
                    json.dump(json_data, json_file)
                    json_done = ''
            print('JSON-file' + json_done + ' записан')

        def execute(self, photos):
            if not photos:
                print('Список Фото не найден')
                return
            self.token = input('Введите токен: ')
            self.ya_folder_path = input('Введите название папки на Яндек диске: ')
            self.create_folder_Ya()
            self.upload_files_Ya(photos)

    vk = Get_max_photo_from_VK()

    vk.execute()

    ya = upload_to_Ya()

    ya.execute(vk.max_photos)
