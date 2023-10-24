import requests
import json
from Yandexdisk import YandexDisk
from pprint import pprint
def http_request():
    url = "https://akabab.github.io/superhero-api/api/all.json"
    response = requests.get(url)
    with open('superheroes.json', 'w', encoding="utf-8") as f:
       json.dump(response.json(), f)

with open('superheroes.json') as f:
    json_data = json.load(f)
    character = {}
for hero in json_data:
    if hero['name'] == "Hulk" or hero['name'] == 'Captain America' or hero['name'] == 'Thanos':
        intelligence = hero['powerstats']['intelligence']
        name = hero['name']
        character[name] = intelligence

def the_best_intelligence(hero):
    filter_dict = [(value, key) for key, value in hero.items()]
    superhero = max(filter_dict)[1]
    return f'Самый умный герой {superhero} c IQ {hero[superhero]}'

if __name__ == '__main__':
    print(the_best_intelligence(character))

    TOKEN = ''
    path_to_file = 'Test_HW'                       # Путь для загрузки и/или имя файла на ЯндексДиске
    file = 'test.txt'                              # Имя файла для загрузки
    my_disk = YandexDisk(TOKEN)                    # Ваш токен
    pprint(my_disk.upload_file(path_to_file, file))
