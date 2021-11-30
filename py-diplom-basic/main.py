# from pprint import pprint
import requests

class Photo_from_VK_to_Ya:
    def __init__(self):
        self.owner_id = input('Введите id пользователя или слово - нет, если нужны фото по текущему пользователю: ')
        self.token = input('Введите токен: ')
        self.cnt = int(input('Введите количество фото для сохранения или цифру - 0, тогда сохранится 5 фото: '))
        self.ya_folder_path = input('Введите название папки на Яндек диске: ')
        self.ya_url = 'https://cloud-api.yandex.net:443'
        self.vk_url = 'https://api.vk.com/method/photos.get?access_token=958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008&v=5.131&album_id=profile&extended=1'
        self.photo_sizes_sort_desc = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'm', 'o', 's']
        self.max_photos = []

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_max_photo_urls_from_VK(self):
        if self.owner_id != 'нет':
            self.vk_url = self.vk_url + '&owner_id=' + self.owner_id
        response = requests.get(url=self.vk_url).json()['response']
        photos_count = response['count']
        if photos_count < 1:
            return {'status': 'error','message': 'Нет фотографий'}
        if self.cnt < 1:
            self.cnt = 5
        if self.cnt > photos_count:
            self.cnt = photos_count
        photos_info = response['items']
        while self.cnt != 0:
            self.cnt = self.cnt-1
            photo_sizes = photos_info[self.cnt]['sizes']
            for size in self.photo_sizes_sort_desc:
                added = False
                for photo_size in photo_sizes:
                    if photo_size['type'] == size:
                        added = True
                        self.max_photos.append({
                            'id':photos_info[self.cnt]['id'],
                            'url':photo_size['url'],
                            'likes':photos_info[self.cnt]['likes']['count']
                        })
                        break
                if added:
                    break
        return ({'status': 'success', 'photos':self.max_photos})

    def create_folder_Ya (self):
        params = {'path': self.ya_folder_path}
        requests.put(url=self.ya_url + '/v1/disk/resources', params = params,  headers=self.get_headers())

    def upload_files_Ya(self):
        for photo in self.max_photos:
            name = str(photo['likes']) + '-' + str(photo['id']) + '.jpg'
            params = {'path': self.ya_folder_path + '/' + name, 'url': photo['url']}
            requests.post(url=self.ya_url + '/v1/disk/resources/upload', params = params, headers = self.get_headers())

    def execute(self):
        response = self.get_max_photo_urls_from_VK()
        if response['status'] == 'error':
            return response['message']
        response = self.create_folder_Ya()
        response = self.upload_files_Ya()
        return 'Фото загружены'

obj = Photo_from_VK_to_Ya()

print(obj.execute())