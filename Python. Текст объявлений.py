'''
Собирает текст объявлений из списка с URL-ами
Вход: файл с URL-ами
Выход: файл <results> со списком текстов
'''

import urllib.request
import re

texts_file = input('Enter file with URLs: ')
results = input('Enter results file: ')

def collect_texts_from_file():
    '''
    Собирает тексты объявлений из URL-ов в файле.
    Вход: текстовый файл 
    Выход: список из текстов
    '''
    print()
    texts_list_raw = []
    texts_list = []
    i = 1
    with open(texts_file, 'r') as f:
        url_list = f.readlines()
    print('Found ' + str(len(url_list)) + ' URLs')
    print('Результаты будут выведены в файл «' + str(results) + '»')
    print()
    for url in url_list:
        flag = 0
        text = ''
        print('Doing URL ' + str(i) + ' out of ' + str(len(url_list)))
        source_page_for_texts = urllib.request.urlopen(url)
        for line in source_page_for_texts:
            line = line.decode('cp1251')
            if 'data-field="text"' in line:
                flag = 1
            elif flag == 1 and '</div>' not in line:
                text += line
            elif flag == 1:
                break
        if text == '':
            texts_list_raw += [url]
        else:
            texts_list_raw.append(text)
        i+=1
    for text in texts_list_raw:
        text = re.sub('<.*>', '', text)
        text = re.sub('\n', '\t', text)
        text = re.sub('\t+', '\t', text)
        text = re.sub('^\t+|\t+$', '', text)
        text = text.replace('&quot;','"')
        text = text.replace('&amp;','&')
        text = text.replace('&shy;','')
        text = text.replace('&gt;','>')
        text = text.replace('&#039;','\'')
        texts_list.append(text)
    return(texts_list)

texts_list = collect_texts_from_file()

with open(results, 'w') as f:
    for text in texts_list:
        f.write(text + '\n')
