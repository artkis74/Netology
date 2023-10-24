import csv
import re


# читаем адресную книгу в формате CSV в список contacts_list
def OpenFile():
    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def get_contacts():
    data = OpenFile()
    phone_list = []
    fields = [data[0][0], data[0][1], data[0][2], data[0][4], data[0][5], data[0][6]]
    phone_list.append(fields)
    pattern = r'[ЁА-Я]\w+'
    for elements in data:
        man_list = []
        for values in elements[0:2]:
            contact = re.findall(pattern, values)
            if len(contact) > 0:
                for names in contact:
                    man_list.append(names)
        if len(man_list) > 0:
            phone_list.append(man_list)
        if len(man_list) != 3:
            for i in range(3 - len(man_list)):
                man_list.append('')
        man_list.extend(elements[4:7])
    return phone_list


def change_numbers():
    data = get_contacts()
    pattern = r'(\+7|8)?(\s*)?(\()?(\d\d\d)(\))?[-\s*]?(\d\d\d)[-\s]*(\d\d)[-\s]*(\d\d)\s*(\()?(\доб.)?\s*(\d*)(\))?'
    suns = r'+7(\4)\6-\7-\8 \10 \11'
    for lists in data:
        for values in lists:
            number = re.findall(pattern, values)
            if len(number) > 0:
                new_number = re.sub(pattern, suns, values)
                lists.pop(-2)
                lists.insert(-1, new_number.strip())
    return data


def get_copys():
    data = change_numbers()
    dict_names = {}
    copy = []
    copy_list = []
    for i in range(1, len(data)):
        if data[i][0:2] not in dict_names.values():
            dict_names[i] = data[i][0:2]
    for items in dict_names.values():
        for elements in data:
            if items[0] in elements and items[1] in elements:
                copy.append(data.index(elements))
        if len(copy) > 1:
            copy_list.append(copy)
        copy = []
    return copy_list


def del_copys():
    list_copys = get_copys()
    copys = []
    data = change_numbers()
    new_data = [data[0]]
    new_lists = []
    for elements in list_copys:
        for items in elements:
            for lists in data:
                if data.index(lists) == items:
                    for i in range(6):
                        if lists[i] not in new_lists and len(lists[i]) > 0:
                            new_lists.append('')
                            if i < len(new_lists):
                                new_lists.pop(i)
                            new_lists.insert(i, lists[i])
        new_data.append(new_lists[0:7])
        new_lists = []
    for p in list_copys:
        copys.extend(p)
    for list_data in data[1:len(data)]:
        if data.index(list_data) not in copys:
            new_data.append(list_data)
    return new_data


# TODO 2: сохраните получившиеся данные в другой файл


if __name__ == "__main__":
    with open("phonebook.csv", "w", encoding='UTF-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(del_copys())
