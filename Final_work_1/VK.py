import requests

with open('vk_data.txt', 'r') as file:
    token = file.readline().strip()
    id_vk = file.readline().strip()
class VK:

   def __init__(self, access_token=token, user_id=id_vk, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def get_photos_prof(self):
       url = 'https://api.vk.com/method/photos.get'
       params = {'user_ids': self.id, 'album_id': 'profile', 'extended': '1'}
       response = requests.get(url, params={**self.params, **params})
       return response.json()
