import requests


class Ya:
    def __init__(self):
        self.ya_url = 'https://cloud-api.yandex.net:443';

    def get_headers(self, token):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(token)
        }

    def create_folder_Ya(self, path, token):
        params = {'path': path}
        res = requests.put(url=self.ya_url + '/v1/disk/resources', params=params,  headers=self.get_headers(token))
        return(res.status_code)

    def delete_folder_Ya(self, path, token):
        params = {'path': path}
        res = requests.delete(url=self.ya_url + '/v1/disk/resources', params=params,  headers=self.get_headers(token))
        return(res.status_code)