'''
Разделяет файл на указанное число подфайлов.
Вход: большой файл
Выход: несколько маленьких файлов
'''

def get_split_file():
    start_line = 0
    file_count = 1
    small_list = []
    big_file = input('Enter your big file here: ')
    small_file_size = int(input('How many lines in small file: '))
    with open(big_file, 'r') as f:
        big_list = f.readlines()
    while True:
        if len(big_list) > start_line+small_file_size:
            end_line = start_line+small_file_size
            is_finish = False
        else:
            end_line = len(big_list)
            is_finish = True
        for line in big_list[start_line:end_line]:
            small_list.append(line)
        small_file_name = 's' + str(file_count)
        with open(small_file_name, 'w') as f:
            for line in small_list:
                f.write(line)
        if is_finish:
            print()
            print('Done.')
            break
        else:
            small_list = []
            file_count+=1
            start_line = end_line
            
get_split_file()
