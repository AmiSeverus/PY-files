import requests

class Get_photo_from_VK:
    def __init__(self):
        self.vk_url = 'https://api.vk.com/method/'
        self.params = '?access_token=e9d323112cddc1440cd28b722a5215b7fdbfa263e8c6a3120e2ca78207c249b93a9424b752e9aeaca10a9&v=5.131&album_id=profile&extended=1'
        self.user_id = ''

    def get_user_id(self, username):
        vk_search_url = self.vk_url + 'utils.resolveScreenName' + self.params + '&screen_name=' + username
        response = requests.get(url=vk_search_url)
        if response.status_code == 200 and 'response' in response.json() and 'type' in response.json()['response']:
            if response.json()['response']['type'] == 'user':
                self.user_id = response.json()['response']['object_id']
                res = {'status':'success'}
            else:
                res = {'status': 'error', 'message': 'По данному username найден не пользователь, а ' + response.json()['response']['type']}
        else:
            res = {'status': 'error', 'message': 'Пользователь не найден'}
        return res

    def get_photo_from_VK(self, url):
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
        vk_url = self.vk_url + 'photos.get' + self.params
        if self.user_id:
            res = self.get_photo_url_from_VK(vk_url + '&owner_id=' + str(self.user_id))
            if res['status'] == 'error':
                print(res['message'])
            else:
                print(f'Фото пользователя {id} найдено')