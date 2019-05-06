'''
Полезно для написания карверов
Циклично удаляет в файле каждую вторую строку до тех пор, пока не получим желаемое количество строк.
Почему нельзя тупо удалить половину файла? — потому что так разнообразия строк будет меньше

Вход: адрес файла
Выход: файл со списком заголовков
'''

start_file = input('Enter your too looooooooooooong file: ') 
number_of_lines_in_result = input('How many lines do you want? Press ENTER to leave default = 4000 lines')

if number_of_lines_in_result == '':
    number_of_lines_in_result = 4000
else:
   number_of_lines_in_result = int(number_of_lines_in_result) 

result = input('Enter result file: ')
print()

with open (start_file, encoding='cp1251') as f:
    sub_list = f.readlines()

i = 0
while True:
    print('There are ' + str(len(sub_list)) + ' lines in file.')
    if len(sub_list)/2 < number_of_lines_in_result:
        break
    del sub_list[::2]
    i += 1

with open(result, 'w') as f:
    for line in sub_list:
        f.write(line)
print()
print('We repeat ' + str(i) + ' times.')
print('There are ' + str(len(sub_list)) + ' lines in file.')
