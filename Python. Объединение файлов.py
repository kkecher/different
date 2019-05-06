'''
Объединяет несколько файлов в один. Файлы должны быть названы числами. Не страшно, если числа будут не все по порядку.
Вход: файлы, названные числами
Выход: один файл
'''
num_files = input('How many files do you have? ')
result_file = input('Enter result file: ')
total_list = []
for file_name in range(1, int(num_files)+1):
    try:
        with open(str(file_name)) as f:
            total_list += f.read().splitlines()
    except:
        continue

with open(result_file, 'w') as f:
    for line in total_list:
        f.write(str(line) + '\n')
