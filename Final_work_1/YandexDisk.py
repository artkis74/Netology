import requests

with open('token_yandex.txt', 'r') as file:
    token_disk = file.readline().strip()


class YandexDisk:
    def __init__(self, token=token_disk):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json',
                'Authorization': f'OAuth {self.token}'}

    def get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file(self, disk_file_path, file):
        href = self.get_upload_link(disk_file_path=disk_file_path)
        response = requests.put(href['href'], data=open(file, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            return "Файл загружен"
        else:
            return f"Ошибка {response.status_code}"

    def create_new_folder(self, disk_file_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": disk_file_path}
        response = requests.put(url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            return f"Папка {disk_file_path} создана!"
        else:
            return f"Ошибка {response.status_code}"
