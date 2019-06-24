'''
Удаляет diff между файлами в одном из файлов.
Вход: два файла; выбор, в каком из файлов удаляем строки
Выход: файл с удаленными диффами
'''
text1 = input('Enter your first dirty file, old bastard: ')
text2 = input('Ahhh, ok, give me your second file, silly faggot: ')
mode = input('Where do you want to delete rows? Enter 1 or 2: ')
result = input('Enter result file: ')


with open(text1, 'r', encoding='utf-8') as f:
    text1_list = f.readlines()

with open(text2, 'r', encoding='utf-8') as f:
    text2_list = f.readlines()

text1_list = sorted(set(text1_list))
text2_list = sorted(set(text2_list))

if mode == '1':
    for line in text2_list:
        try:
            text1_list.remove(line)
        except:
            continue
else:
    for line in text1_list:
        try:
            text2_list.remove(line)
        except:
            continue
 
with open(result, 'w') as f:
    if mode == '1':
        for line in text1_list:
            f.write(line)
    else:
        for line in text2_list:
            f.write(line)
