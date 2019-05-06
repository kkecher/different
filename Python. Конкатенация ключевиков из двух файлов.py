'''
Эта программа объединяет ключевики из двух файлов (берет строку из одного файла и прописывает ее к каждой строке второго)
Вход: 2 файла с ключевиками
Выход: файл с объединенными ключевиками
'''

key_file1 = input('Enter first file: ')
key_file2 = input('Enter second file: ')
result = input('Enter result file: ')

print()
print('Results will be written in file «' + str(result) + '»')
print()

with open(key_file1) as f:
    key_list1 = f.readlines()
    len_key_list1 = len(key_list1)

with open(key_file2) as f:
    key_list2 = f.readlines()
    len_key_list2 = len(key_list2)

def concatinate_keys():
    '''
    Объединяет ключевики из двух файлов (берет строку из одного файла и прописывает ее к каждой строке второго)
    Вход: 2 файла с ключевиками
    Выход: файл с объединенными ключевиками
    '''
    with open(result, 'w') as f:
        #Считаем общее количество итоговых ключевиков для расчета прогресса
        i = 0
        key_total = len_key_list1 * len_key_list2

        #Объединяем ключевики с двух файлов
        for key1 in key_list1:
            key1= key1[:-1] #убираем перенос в конце
            for key2 in key_list2:
                key2 = key2[:-1]
                key_res = str(key1) + ' ' + str(key2)
                f.write(key_res + '\n')
                i += 1
                current_percent = round(i / key_total*100, 2)
                print(str(current_percent) + '%')

concatinate_keys()
print()
print ('I\'v completed you dirty wish, ugly old bastard!')
