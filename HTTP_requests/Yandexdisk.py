import requests

class YandexDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json','Accept': 'application/json',
                'Authorization': f'OAuth {self.token}'}

    def __get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file(self, disk_file_path, file):
        href = self.__get_upload_link(disk_file_path=disk_file_path)
        response = requests.put(href['href'], data=open(file))
        response.raise_for_status()
        if response.status_code == 201:
            return "Фаил загружен"
        else:
            return f"Ошибка {response.status_code}"