'''
Вносит в справочник запчастей склонения лемм
Вход: файл «Склонения.txt» со списком склонений в формате JSON; файл «Справочник. Исходный.txt» со справочником лемм запчастей
Выход: файл «results» со справочником лемм запчастей, куда на место первого и второго синонимов занесены склонения лемм.

РЕЗУЛЬТАТ НУЖДАЕТСЯ В ПРОВЕРКЕ, ТАК КАК ЧАСТЬ СКЛОНЕНИЙ НЕКОРРЕКТНЫ
'''

import json

def get_lemma_without_synonyms():
    '''
    Загружает леммы из справочника запчастей и вычленяет названия лемм, собирает их в список list_lemmas_without_synonyms. Леммы из списка используются в функции get_skl() для получения склонений
    Вход: файл «Справочник. Исходный.txt» со справочником лемм запчастей
    Выход: список лемм запчастей без синонимов
    '''
    lemma_without_synonyms = ''
    list_lemmas_without_synonyms = []
    with open('Справочник. Исходный.txt', 'r') as f:
        list_lemma = f.readlines()
    for lemma in list_lemma:
        is_plus = False
        for letter in lemma:
            if letter in '#':
                break
            if letter in '?!':
                continue
            if letter in '+':
                is_plus = True
                continue
            if letter in ['(', ',', '\n', ')']:
                if letter in '(' and is_plus:
                    continue
                if letter in ')' and is_plus:
                    is_plus = False
                    continue
                list_lemmas_without_synonyms.append(lemma_without_synonyms)
                lemma_without_synonyms = ''
                break
            else:
                lemma_without_synonyms+= letter
#    Печатаем список лемм без синонимов для дебага
#    i = 1 
#    for lemma in list_lemmas_without_synonyms:
#        print(str(i) + '. ' + lemma)
#        i+=1
    return(list_lemmas_without_synonyms)

# Получаем список лемм без синонимов для дебага
#list_lemmas_without_synonyms = get_lemma_without_synonyms()

def get_skl(lemma, padezh, chislo='ed'):
    '''
    Получает склонения для указанной леммы в указанном падеже и числе
    Вход: лемма, падеж, число (по-умолчанию — единственное)
    Выход: лемма в указанном падеже и числе.
    '''
    with open('Склонения.txt', 'r') as f:
        str_skl = f.read()
    dict_skl = json.loads(str_skl)
    if chislo == 'ed':
        try:
            return(dict_skl.get(lemma).get(padezh))
        except:
            return('АХТУНГ!!!')
    else:
        try:
            return(dict_skl.get(lemma).get('множественное').get(padezh))
        except:
            try:
                if(dict_skl.get(lemma).get(padezh)) is None: #обрабатывает случай, когда исходная лемма написана во мн. числе
                    return(lemma)
                else:
                    return(dict_skl.get(lemma).get(padezh))
            except:
                return('АХТУНГ!!!')

def insert_skl():
    '''
    Вносит собранные в функции get_skl склонения в справочник на место первого и второго синонимов
    Вход: справочник запчастей «Справочник. Исходный.txt»
    Выход: список лемм с записанными синонимами
    ПОРЯДОК ЛЕММ В СПРАВОЧНИКЕ ЗАПЧАСТЕЙ ДОЛЖЕН СОВПАДАТЬ С ПОРЯДКОМ ЛЕММ ИЗ СПРАВОЧНИКА, ИСПОЛЬЗОВАВШЕГОСЯ В ФУНКЦИИ get_lemma_without_synonyms (знаю, можно доработать, но нахуя)
    '''
    list_lemmas_without_synonyms = get_lemma_without_synonyms()
    list_lemmas_with_skl = []
    with open('Справочник. Исходный.txt', 'r') as f:
        list_lemma = f.readlines()
    lemma_count = 0
    for lemma in list_lemma:
        print('Doing ' + str(lemma_count) + ' of ' + str(len(list_lemma)))
        letter_count = 0
        part_lemma_before_skl = ''
        for letter in lemma:
            if letter in '#':
                list_lemmas_with_skl.append(lemma)                
                break
            if letter in [',', '\n']:
                lemma_without_synonyms = list_lemmas_without_synonyms[lemma_count]
                lemma_without_synonyms = lemma_without_synonyms.rstrip() #убираем пробел в конце, если он попал сюда
                lemma_vinitelny_ed = get_skl(lemma_without_synonyms, 'В')
                lemma_imenitelny_mn = get_skl(lemma_without_synonyms, 'И', 'mn')

                #печатаем лемму и ее склонения для дебага
                if 'АХТУНГ' in lemma_vinitelny_ed or 'АХТУНГ' in lemma_imenitelny_mn:
                    print(lemma_without_synonyms)
                    print(lemma_vinitelny_ed)
                    print(lemma_imenitelny_mn)
                    print()

                lemma_with_skl = part_lemma_before_skl + ', $$$' + lemma_vinitelny_ed + ', ' + lemma_imenitelny_mn + '$$$' + lemma[letter_count:]
                list_lemmas_with_skl.append(lemma_with_skl)
                lemma_count+=1
                break
            else:
                part_lemma_before_skl+=letter
                letter_count+=1
    print('Get list with ' + str(len(list_lemmas_with_skl)) + ' lemmas')
    return(list_lemmas_with_skl)

list_lemmas_with_skl = insert_skl()

with open('results', 'w') as f:
    for lemma in list_lemmas_with_skl:
        f.write(lemma)
