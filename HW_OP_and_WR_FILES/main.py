import os
from pprint import pprint

with open('recipes.txt', encoding='utf-8') as file:
    cook_book = {}
    for line in file:
        dish = line.strip()
        ingredients = []
        for ingredient in range(int(file.readline())):
            # print(ingredient)
            ingredient_dict = {}
            ingredient_name, quantity, measure = file.readline().split('|')
            ingredient_dict['ingredient_name'] = ingredient_name.strip("/n")
            ingredient_dict['quantity'] = quantity.strip("/n")
            ingredient_dict['measure'] = measure.strip("/n")
            ingredients.append(ingredient_dict)
            cook_book[dish] = ingredients
        file.readline()
# pprint(cook_book)


def get_shop_list_by_dishes(dishes, person_count):
    for dish in dishes:
        if dish not in list(cook_book.keys()):
            return 'Такого блюда нет'
        shop_list = {}
    for key, values in cook_book.items():
            # print(value)
        if key in dishes:
            for ingredient in values:
                ingredient['quantity'] = int(ingredient['quantity']) * person_count
                ingredient['measure'] = ingredient['measure'].rstrip()
                if ingredient['ingredient_name'] not in shop_list.keys():
                    shop_list[ingredient['ingredient_name']] = {k: v for k, v in ingredient.items()
                    if k !='ingredient_name'}
                else:
                    for quant in shop_list.values():
                        for value in quant.keys():
                            if value == quantity:
                                value["quantity"] = int(value['quantity']) + ingredient['quantity']
    return shop_list

# pprint(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'],2))


dict = {}
ROOT_PATH = os.getcwd()
FILE_LOG_DIR = 'Files'
files_list = os.listdir(os.path.join(ROOT_PATH, FILE_LOG_DIR))
for file in files_list:
    path = os.path.join(ROOT_PATH, FILE_LOG_DIR, file)
    with open(path, encoding='utf-8') as content:
        text = []
        for string in content:
            text.append(string.strip())
            lens = len(text)
        dict[file] = [len(text), text]
sorted_list = sorted(dict.items(), key=lambda item: item[1])

with open('final file.txt', 'w+', encoding='utf-8') as f:
    for strings in sorted_list:
        f.write(strings[0]+'\n')
        f.write(str(strings[1][0]) + '\n')
        for sentence in strings[1][1]:
            str_ = ''.join(str(x) for x in sentence)
            f.write(str_ + '\n')
