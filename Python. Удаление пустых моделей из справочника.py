'''
Удаляем из справочника леммы, присутствующие в файле
Вход: файл со списком моделей без актуальных и архивных предложений; файл со справочником леммакса
Выход: файл со справочником леммакса, где удалены пустые модели («Пустые модели. Измененный справочник.txt»); файл с удаленными моделями («Пустые модели. Удалены.txt»); файл с НЕудаленными моделями («Пустые модели. Остались.txt»)
'''

def delete_lemma():
    '''
    Создает новый справочник леммакса без пустых моделей.
    Вход: файл со справочником леммакса; файл с пустыми моделями
    Выход: список со справочником леммакса, где удалены пустые модели; список с удаленными моделями; список с НЕудаленными моделями
    '''
    lemma_without_synonyms = ''
    lemma_without_killed_list = []
    killed_lemma_list= []
    not_killed_lemma_list= []
    killed_lemma_count = 0
    empty_model = input('Enter file with empty models: ')
    lemma_lemmax_dict = input('Enter file with lemma\'s lemmax dict: ')
    with open(empty_model, 'r') as f:
        empty_model_list = f.read().splitlines()
    empty_model_list = [model.lower() for model in empty_model_list] #Переводим в lowercase все модели    
    with open(lemma_lemmax_dict, 'r', encoding='utf-8') as f:
        lemma_list = f.readlines()
    for lemma in lemma_list:
        is_plus = False
        letter_pos = 0
        for letter in lemma:
            if letter in '#':
                lemma_without_killed_list.append(lemma)
                break
            if letter in '?!)':
                letter_pos+=1
                continue
            if letter in '+' and lemma[letter_pos+1] == '(':
                is_plus = True
                letter_pos+=1
                continue
            if letter in ['(', ',', '\n']:
                if letter in '(' and is_plus:
                    letter_pos+=1
                    is_plus = False
                    continue
                lemma_without_synonyms = lemma_without_synonyms.rstrip() 
                if lemma_without_synonyms.lower() not in empty_model_list:
                    print(lemma_without_synonyms + ' - alive')
                    lemma_without_killed_list.append(lemma)
                    not_killed_lemma_list.append(lemma_without_synonyms)
                else:
                    print(lemma_without_synonyms + ' WAS KILLED! AHAHAHA')
                    killed_lemma_count+=1
                    killed_lemma_list.append(lemma_without_synonyms)
                lemma_without_synonyms = ''
                break
            else:
                lemma_without_synonyms+= letter
    print()
    print('We killed ' + str(killed_lemma_count) + ' of ' + str(len(empty_model_list)) + ' lemmas.')
    return(lemma_without_killed_list, killed_lemma_list, not_killed_lemma_list)

lemma_without_killed_list, killed_lemma_list, not_killed_lemma_list = delete_lemma()

with open('Пустые модели. Измененный справочник.txt', 'w') as f:
    for lemma in lemma_without_killed_list:
        f.write(lemma)

with open('Пустые модели. Удалены.txt', 'w') as f:
    for lemma in killed_lemma_list:
        f.write(lemma + '\n')

with open('Пустые модели. Остались.txt', 'w') as f:
    for lemma in not_killed_lemma_list:
        f.write(lemma + '\n')
