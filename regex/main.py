from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re


with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код


cnt = 1

FI = []

while cnt < len(contacts_list):
    contact = contacts_list[cnt]
    if (contact[5]):
        contact[5] = re.sub(r'(\+7|8)?\s?[(]?\s?(\d{3})[)]?\s?[-]?(\d{3})\s?[-]?(\d{2})\s?[-]?(\d{2})', r"+7(\2)\3-\4-\5", contact[5])
        if len(contact[5]) > 16:
            contact[5] = re.sub(r'[(]?доб.\s?(\d{4})[)]?', r"доб.\1", contact[5])
    if contact[0].strip().find(' ') > -1:
        name_list = contact[0].split(' ')
        index = 0
        while index < len(name_list):
            if (name_list[index]):
                contact[index] = name_list[index]
            index += 1
    if contact[1].strip().find(' ') > -1:
        name_list = contact[1].split(' ')
        index = 0
        while index < len(name_list):
            if (name_list[index]):
                contact[index+1] = name_list[index]
            index += 1
    if contact[0]+contact[1] in FI:
        orig_cnt = FI.index(contact[0]+contact[1]) + 1
        index = 2
        while index < 7:
            if contact[index]:
                contacts_list[orig_cnt][index] = contact[index]
            index += 1
        contacts_list.pop(cnt)
    else:    
        FI.append(contact[0]+contact[1])
        cnt += 1

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)