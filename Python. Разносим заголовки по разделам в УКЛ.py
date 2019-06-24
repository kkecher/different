#!/usr/bin/env python3
# coding= utf8

'''
Распределяет вводы по разделам согласно регуляркам из ucl_file
Вход: ucl_file с регулярками, файл с заголовками
Выход: файл с распределением заголовков по разделам

Note: изначально я проходил по регуляркам в цикле без re.compile, но вышло ОЧЕНЬ долго (24000 заголовков обрабатывались 2,5 часа). Потом попробовал re.compile. Время сократилось до 5 минут:D
'''

import re
import timeit

start_time = timeit.default_timer()

#загружаем список заголовков
#subjects_file = input('Enter file with subjects: ')
subjects_file = 'Масла трансмиссионные. ATF.txt'
with open(subjects_file, 'r', encoding='utf-8') as f:
    subjects_list = f.read().splitlines()

#обозначаем файл с результатами
#result_file = input('Enter result file: ')
result_file = 'res'

#загружаем список соответствий id раздела - название раздела, чтобы в итоге выводить названия разделов, а не только id
#id_and_name_of_dirs_file = input('Enter file with id-name of dirs: ')
id_and_name_of_dirs_file = 'Масла. id и названия разделов.txt'
with open(id_and_name_of_dirs_file, 'r', encoding='utf-8') as f:
    id_and_name_of_dirs_list = f.read().splitlines()

#создаем словарь; key=id раздела, value=название раздела
id_and_name_of_dirs_dict = {}
for line in id_and_name_of_dirs_list:
    line_id_and_name_of_dirs_list = line.split(' — ')
    dir_id = line_id_and_name_of_dirs_list[0].strip()
    dir_name = line_id_and_name_of_dirs_list[1].strip()
    id_and_name_of_dirs_dict[dir_id] = dir_name

#создаем список с регулярками и id разделов
#ucl_file = input('Enter UCL file: ')
ucl_file = 'Масла. УКЛ с текущими регулярками.txt'
with open(ucl_file, 'r', encoding='utf-8') as f:
    regex_dict = {} #создаем словать с регулярками; key=id раздела, value=кортеж (<регулярка>, <номер строки с регуляркой>)
    line_iter = 1 #считаем номер регулярки, чтобы выводить его рядом с заголовком. Поможет быстро найти, по какой регулярке заголовок попал в этот раздел
    for line in f:
        line = line.rstrip() #убираем пробелы и знаки переносов в конце
        line = re.sub(r'^"', '', line, flags=re.IGNORECASE) #убираем кавычки с начала строки
        line = re.sub(r'^\/', '', line, flags=re.IGNORECASE)  #убираем / с начала строки
        line = re.sub(r', "autoparts"', '', line, flags=re.IGNORECASE) #убираем "autoparts"
        line = re.sub(r", 'autoparts'", '', line, flags=re.IGNORECASE) #убираем 'autoparts'. Таких сейчас нет, но вдруг
        line = re.sub(r'\/", ', ', ', line, flags=re.IGNORECASE) #убираем /", в конце
        line = re.sub(r'", ', ', ', line, flags=re.IGNORECASE)  #убираем ", в конце

        #если строка содержит регулярку, то обновляем словарь regex_dict; key=dir_id, value=кортеж (<регулярка>, <номер строки с регуляркой>):
        is_regex = re.search(r'(^.*),\s?(\d+$)', line, flags=re.IGNORECASE)
        if is_regex:
            regex = is_regex.group(1).strip()
            try: #проверяем, корректна ли регулярка (могут быть пропущены скобки и прочее). На этом этапе, пока мы обрабатываем регулярки по одной, найти ошибку гораздо проще.
                re.compile(regex)
            except re.error:
                print()
                print()
                print(str(line_iter), regex)
                print()
                print()
                raise
            dir_id = is_regex.group(2).strip()
            regex_with_regex_iter_tuple = (regex, line_iter)
            regex_dict.setdefault(dir_id, []).append(regex_with_regex_iter_tuple)
        line_iter+=1


#Создаем из regex_dict словарь с компилированными регулярками; key=id раздела, value=компилированная регулярка для этого раздела. Note: re.compile значительно ускоряет работу программы. Словарь compiled_regex_dict будем использовать для определения, попадает ли вообще заголовок в этот раздел. Если попадает, то используем раннее созданный словарь regex_dict для определения номера регулярки, по которой распознался заголовок.
regex_compiled_dict = {}
for dir_id in regex_dict:
    regex_list = [] #список регулярок для данного id. Получаем из кортежей словаря regex_dict
    regex_with_regex_iter_list = regex_dict[dir_id]
    for regex_with_regex_iter_tuple in regex_with_regex_iter_list:
        regex = regex_with_regex_iter_tuple[0]
        regex_list.append(regex)
    regex_string = '|'.join(regex_list)
    regex_compiled = re.compile(regex_string, flags=re.IGNORECASE)
    regex_compiled_dict[dir_id] = regex_compiled

def is_match_regex_compiled(subject, dir_id):
    regex = regex_compiled_dict[dir_id]
    is_match = re.search(regex, subject)
    return(is_match)

def collect_subjects_matched_to_dir_id_regexes(subject, dir_id):
    subject_regex_iter_dict = {}
    regex_list = regex_dict[dir_id]
    for regex_with_regex_iter_tuple in regex_list:
        regex = regex_with_regex_iter_tuple[0]
        regex_iter = regex_with_regex_iter_tuple[1]
        #print(regex, regex_iter) #debug
        if re.search(regex, subject, flags=re.IGNORECASE):
            subject_regex_iter_dict.setdefault(subject, []).append(regex_iter)
    return(subject_regex_iter_dict)

#идем по заголовкам, если заголовок соответствует регулярке, то записываем заголовок в словарь
subjects_filtered_by_dirs_dict = {} #создаем словарь; key=id раздела, value=словарь {key=заголовок, value=список номеров строк регулярок}
subjects_match_more_than_1_id_dict = {} #создаем словарь; key=subject, value=список id разделов, в которых находится заголовок. Изначально сюда пишутся ВСЕ id, даже если заголовок был только в этом одном id раздела (что противоречит названию переменной). Но я не хочу создавать еще одно условие:(
subject_iter = 1
len_subjects_list = len(subjects_list)
for subject in subjects_list:
    is_match_dir_id = False
    print('Doing ' + str(subject_iter) + ' of ' + str(len_subjects_list) + ' subjects')
    for dir_id in regex_dict:
        if is_match_regex_compiled(subject, dir_id):
            is_match_dir_id = True #если заголовок распознался регулярками раздела, то НЕ добавляем его потом в список «Нет соответствий»
            subject_regex_iter_dict = collect_subjects_matched_to_dir_id_regexes(subject, dir_id)
            subjects_filtered_by_dirs_dict.setdefault(dir_id, {}).update(subject_regex_iter_dict)
            subjects_match_more_than_1_id_dict.setdefault(subject, []).append(dir_id) #сюда пока записываем ВСЕ id разделов, которым соответствует заголовок (даже если заголовок соответствует всего одному id). Потом оставлю уникальные значения и возьму заголовки, где число id>1. Не хочу вводить еще одно условие, и так хер разберешь уже:(
    if not is_match_dir_id:
        subject_regex_iter_dict = {subject: [None]}
        subjects_filtered_by_dirs_dict.setdefault('Нет соответствий', {}).update(subject_regex_iter_dict)
    subject_iter+=1

#записываем в файл полученные соответствия id-заголовок и название раздела
with open(result_file, 'w') as f:
    for dir_id, subject_regex_iter_dict in subjects_filtered_by_dirs_dict.items():
        if dir_id in id_and_name_of_dirs_dict: #если id раздела есть в списке id-название, то получаем название раздела
            dir_name = id_and_name_of_dirs_dict[dir_id]
            f.write(str(dir_name) + ' (' + str(dir_id) + ')' + '\n')
        elif dir_id != 'Нет соответствий': #если id нет в списке id-название и id НЕ равен «Нет соответствия», то пишем в файл предупреждение
            f.write('АХТУНГ! - НЕТ НАЗВАНИЯ РАЗДЕЛА' + ' (' + str(dir_id) + ')' + '\n')
        else:
            f.write(dir_id + '\n') #dir_id = Нет соответствия
        f.write('#'*50 + '\n')
        for subject, regex_iter_list in subject_regex_iter_dict.items():
            f.write(str(subject) + ' ### ')
            is_first_regex_iter = True
            for regex_iter in regex_iter_list:
                if is_first_regex_iter:
                    f.write(str(regex_iter))
                    is_first_regex_iter = False
                else:
                    f.write(', ' + str(regex_iter))
            f.write(' - numbers of regex lines')
            f.write('\n')
        f.write('\n'*2)
    f.write('\n'*5)

    #записываем заголовки, которые соответствуют более, чем одному id
    f.write('Заголовки соответствуют более, чем одному id' + '\n')
    f.write('#'*50 + '\n')
    for subject, dir_id_list in subjects_match_more_than_1_id_dict.items():
            dir_id_set = set(dir_id_list) #оставляем уникальные id разделов
            if len(dir_id_set) > 1:
                is_first_dir_id = True #при первом dir_id НЕ дописываем запятую перед названием раздела, чтобы не получить «##### ,»
                f.write(str(subject) + ' ##### ')
                for dir_id in dir_id_set:
                    dir_name = id_and_name_of_dirs_dict[dir_id]
                    if is_first_dir_id:
                        f.write(str(dir_name) + ' (' + str(dir_id) + ')')
                        is_first_dir_id = False
                    else:
                        f.write(', ' + str(dir_name) + ' (' + str(dir_id) + ')')
                f.write('\n')

stop_time = timeit.default_timer()
program_time = stop_time-start_time
program_time_hour = int(program_time // 3600)
program_time_min = int((program_time - program_time_hour*3600) // 60)
program_time_sec = int(program_time - program_time_min*60)

print()
print('I\'ve finished your dirty wish.')
print('It took ' + str(program_time_hour) + ':' + str(program_time_min) + ':' + str(program_time_sec) + ' of my life, silly bastard.')
