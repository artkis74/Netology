import json
import urllib.request
from VK import VK
from pprint import pprint
from YandexDisk import YandexDisk
from datetime import datetime

if __name__ == '__main__':
    my_disk = YandexDisk()
    folder = "Final_work#1"
    print(my_disk.create_new_folder(folder))
    vk = VK()
    answer = vk.get_photos_prof()
    images = []
    for data in answer['response']['items']:
        data_image = {}
        link = ' '.join([url['url'] for url in data['sizes'] if url['type'] == 'z'])
        date = data['date']
        # date = datetime.utcfromtimestamp(data['date']).strftime('%Y-%m-%d %H:%M:%S') При таком варианте выдает
        # ошибку  'Specified path "08:01.jpg" has incorrect format', поэтому решил оставить Unix-время
        image_name = str(data['likes']['count'])
        if image_name + '.jpg' in ([image["file_name"] for image in images]):
            data_image["file_name"] = image_name + " " + str(date) + '.jpg'
        else:
            data_image["file_name"] = image_name + '.jpg'
        data_image["size"] = ' '.join([url['type'] for url in data['sizes'] if url['url'] == link])
        images.append(data_image)
        with open("images.json", 'w') as doc:
            json.dump(images, doc)
        urllib.request.urlretrieve(link, "photo.jpg")
        path_to_file = folder + '/' + data_image["file_name"]
        file = "photo.jpg"
        pprint(my_disk.upload_file(path_to_file, file))
