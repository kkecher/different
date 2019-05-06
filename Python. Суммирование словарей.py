'''
Берет файл со списком словарей, объединяет их в один и суммирует каунты
Вход: файл со словарями
Выход: объединенный словарь с суммой каунтов
'''

import json

dict_total = {}

file_with_dict = input('Enter file with dictionaries: ')
result_file = input('Enter result file: ')

with open(file_with_dict, 'r') as f:
    list_with_dict = f.read().splitlines()

for line in list_with_dict:
    line_dict = json.loads(line)
    for model, count in line_dict.items():
        if model in dict_total:
            dict_total.get(model)['count_add'] += count.get('count_add') 
        else:
            dict_total[model] = count

with open('result', 'w') as f:
    for model, count in dict_total.items():
        count_add = count.get('count_add')
        f.write(model + '\t' + str(count_add) + '\n')
