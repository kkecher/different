#!/usr/bin/env python3

'''
Собирает заголовки объявлений из API низкоуровневого поиска. API отдает максимум 50000 записей. Решил, что буду собирать сразу отдельно объявления и товары, чтобы не усложнять логику. Если даже с таким делением предложений больше 50000, то идем по всем городам.
Вход: URL низкоуровневого поиска (обычного, НЕ API)
Выход: файл со списком заголовков
'''

import urllib.request
import json
import re
import timeit

#search_url = input('Введите URL низкоуровневого поиска: ')
search_url = 'http://search-ui.srv.loc/search?agentId=&attributes=&clientId=&command=undefined&facetingAttributes=&filter=&itemsPerPage=50&pageNumber=1&query=directoryId%3D49&sort=&zone=default'

#results = input('Введите файл с результатами: ')
results = 'res'

start_time = timeit.default_timer()

subjects_list = [] #список с заголовками
itemsPerPage = 10000 #число результатов на странице

#выделяем из search_url URL для API низкоуровневого поиска
params_url_list = re.search(r'^.*(\?.*)(&itemsPerPage=)\d+(.*)(&pageNumber=)\d+(.*)', search_url, flags=re.IGNORECASE)
param_itemsPerPage = params_url_list.group(2) + str(itemsPerPage) #меняем количество выводимых результатов на странице на 500. По умолчанию стоит 50
param_pageNumber = params_url_list.group(4)
params_url = params_url_list.group(1) + params_url_list.group(3) + params_url_list.group(5) + param_itemsPerPage #формируем часть урла с неизменяемыми параметрами + param_itemsPerPage. Потом будем дописывать сюда еще номер страницы.
subject_api_url = 'http://search-ui.srv.loc/api/search/' + params_url

#загружаем id городов с внешнего файла
city_id_file = 'd:\OneDrive\Документы\Фарпост\Archive\Города. id.txt'
with open(city_id_file, 'r') as f:
    city_id_list = f.read().splitlines()

open(results, 'w').close()

def get_url_count(type_param=''):
    '''
    Получаем число предложений для введенного URL'а. Если их >50000, то будем собирать каунты по городам.
    Вход: URL для API низкоуровневого поиска
    Выход: число предложений в введеном урле
    Note: нет, выделить id раздела и вставлять его сюда нельзя. Так как может быть нужно собрать заголовки, содержащие какое-то слово, например.
    '''
    type_param_url = '&type%3D' + str(type_param) #часть урла для типа предложения (bulletin или good)
    count_api_url = 'http://search-actual.srv.loc/rest/v1.4/count' + params_url + type_param_url
    print(count_api_url)
    input('enter')
    source_page_for_count = urllib.request.urlopen(count_api_url)
    count = int(source_page_for_count.read())
    return(count)

def get_dir_subjects(count, type_param='', city_param=''):
    '''
    Собирает заголовки из API низкоуровневого поиска с учетом типа
    Вход: часть урла низкоуровневого поиска с параметрами
    Выход: список заголовков
    Note: я специально НЕ написал дефолтное значение для каунт, чтобы не забыть его пересчитать для очередного if
    '''
    subjects_list = []
    total_page_count = count // itemsPerPage + 1
    page_param_url = param_pageNumber
    type_param_url = '&type%3D' + str(type_param) #часть урла для типа предложения (bulletin или good)
    city_param_url = '&cityId%3D' + str(city_param) #часть урла для id города
    for page_iter in range(total_page_count):
        page_iter+=1
        print(f'Doing {page_iter} of {total_page_count}')
        subject_api_url = 'http://search-ui.srv.loc/api/search/' + params_url + type_param_url + city_param_url + page_param_url + str(page_iter)
        temp_subjects_byte = urllib.request.urlopen(subject_api_url)
        temp_subjects_str = temp_subjects_byte.read().decode('utf-8')
        temp_subjects_dict = json.loads(temp_subjects_str)
        temp_subjects_list = temp_subjects_dict['documents']
        for subject_dict in temp_subjects_list:
            subject = subject_dict['subject']
            subjects_list.append(subject)
    return(subjects_list)

#проверяем, если ли в исходном урле параметр по типу предложения. Если есть, то будем собирать заголовки только для этого типа
if '%20type' in search_url or '&type' in search_url:
    is_contain_type = True
else:
    is_contain_type = False
print('search_url', search_url)
print(is_contain_type)

#проверяем, есть ли в исходном урле параметр по городу. Если есть, то будем собирать заголовки только для этого города
if '%20cityId' in search_url or '&cityId' in search_url:
    is_contain_city = True
else:
    is_contain_city = False

#получаем каунт для исходного урла
if is_contain_type:
    print('96')
    count = get_url_count()
    if count > 50000:
        print('Оу, тут больше 50000 предложений. Я пройдусь по городам, но не факт, что соберу ВСЕ заголовки.')
        print()
        city_iter = 1
        for city_id in city_id_list:
            print(f'Doing {city_iter} of {len(city_id_list)}')
            print()
            subjects_list += get_dir_subjects(city_param=city_id, count=count)
            city_iter+=1
    else:
        subjects_list += get_dir_subjects(count=count)
elif is_contain_city:
    print('110')
    count = get_url_count(type_param='bulletin')
    if count>50000:
        print('Оу, тут больше 50000 предожений. Я не смогу собрать только 50000 заголовков объявлений для этого города:(')
        print()
    subjects_list += get_dir_subjects(type_param='bulletin', count=count)
    count = get_url_count(type_param='good')
    if count>50000:
        print('Оу, тут больше 50000 предожений. Я не смогу собрать только 50000 заголовков товаров для этого города:(')
    subjects_list += get_dir_subjects(type_param='good', count=count)
else:
    print('120')
    count = get_url_count('bulletin')
    if count > 50000:
        print('Оу, тут больше 50000 предложений. Я пройдусь по городам, но не факт, что соберу ВСЕ заголовки.')
        print()
        for city_id in city_id_list:
            subjects_list += get_dir_subjects(type_param='bulletin', count=count)
    else:
        subjects_list = get_dir_subjects(type_param='bulletin', count=count)
        print(subjects_list)
    count = get_url_count(type_param='good')
    if count > 50000:
        print('Оу, тут больше 50000 предложений. Я пройдусь по городам, но не факт, что соберу ВСЕ заголовки.')
        print()
        for city_id in city_id_list:
            subjects_list += get_dir_subjects(type_param='good', count=count)
    else:
        subjects_list += get_dir_subjects(type_param='good', count=count)

with open(results, 'a') as f:
    for subject in subjects_list:
        f.write(subject + '\n')

print()
stop_time = timeit.default_timer()
program_time = stop_time-start_time
program_time_hour = int(program_time // 3600)
program_time_min = int((program_time - program_time_hour*3600) // 60)
program_time_sec = int(round(program_time - program_time_min*60,0))
print(f'It took {program_time_hour}:{program_time_min}:{program_time_sec} of my life, silly bastard!') 
print()
