'''
Собирает склонения с сайта morpher.ru
Вход: файл «Леммы» со списком лемм
Выход: файл «Склонения» со списком склонений
Поменять: список лемм в файле «Леммы»
'''

import json, requests

url = "https://ws3.morpher.ru/russian/declension"

with open('Леммы.txt', 'r') as f: #Записываем леммы из файла в список без символов новой строки
    lemma_list = f.read().splitlines()
len_lemma_list = len(lemma_list)

start_line = input('Enter number of start line. Leave empty to parse from first line: ')
end_line = input('Enter number of end line. Leave empty to parse to the end: ')
if start_line == '':
    start_line = 1
if end_line == '':
    end_line = len_lemma_list + 1
i = int(start_line)

for lemma in lemma_list[int(start_line)-1:int(end_line)-1]:
    try:
        dict_skl = {} #Словать, в котором собираются склонения
        params = dict ( #параметры с сайта http://morpher.ru/ws3/python/
            s=lemma,
            format="json",
            #token= #Не обязателен. Подробнее: http://morpher.ru/ws3/#authentication
            )
        response = requests.get(url=url, params=params)
        dict_lemma_skl = json.loads(response.text)
        dict_skl[lemma] = dict_lemma_skl #Добавляем в склонения родителя-лемму
        json_skl = json.dumps(dict_skl, ensure_ascii=False) #Переводим словать в JSON для записи в файл
        with open('Склонения', 'a') as f:
            f.write(json_skl + '\n')
        print(str(i) + ' of ' + str(len_lemma_list) + '. ' + lemma + ' - Успех')
        i+=1
    except:
        dict_skl = {}
        print(str(i) + ' of ' + str(len_lemma_list) + '. ' + lemma + ' - Ахтунг!!!')
        i+=1
