'''
Собирает население городов из Википедии
Вход: список названий городов
Выход: файл с населением

ВАЖНО!!!
— Нужно руками проверить данные для названий, состоящих НЕ из одного слова, так как могут быть переходы на ложные страницы
— Иногда собираются некорректные данные из некоторых чисел — нужно валидировать данные после сбора.
'''

import urllib.request
import urllib.parse
import re

city_list = input('Enter file with cities: ')
result = input('Enter result file: ')

with open(city_list, 'r') as f:
    city_list = f.read().splitlines()

open(result, 'w').close()

i = 1
for city in city_list:
    print ('Doing ' + str(i) + ' of ' + str(len(city_list)) + '. ' + city)
    try:
        url = 'https://ru.wikipedia.org/wiki/' + city
        source_page_for_page_total = urllib.request.urlopen(url)
        for line in source_page_for_page_total:
            city_id_list = re.findall('font-size: larger.*?span>(.*?)<sup id="cite_ref', line.decode('utf-8'))
            if city_id_list != []:
                city_id = city_id_list[0]
                break
        city_id = city_id_list[0]
    except KeyboardInterrupt:
        raise
    except:
        print('АХТУНГ!!!')
        city_id = 'АХТУНГ!!!'
    i += 1
    with open(result, 'a') as f:
        f.write(str(city_id) + '\n')
