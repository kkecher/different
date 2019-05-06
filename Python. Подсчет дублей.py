'''
Считает дубли строк в файле
Вход: любой файл со строками
Выход: строки с числом их дублей
'''

import operator

text = input('Enter file with your dirty text, faggot: ')
result = input('Enter result file: ')

with open(text, 'r') as f:
    text_list = f.read().splitlines()

text_dict = {}
for line in text_list:
    text_dict[line] = text_dict.get(line, 0) + 1

text_sorted_dict = sorted(text_dict.items(), key=operator.itemgetter(1), reverse=True)

with open(result, 'w') as f:
    for text_tuple in text_sorted_dict:
            f.write(str(text_tuple[1]) + ' - ' + str(text_tuple[0]) + '\n')

