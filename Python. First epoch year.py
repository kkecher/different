'''
Вычисляет начальный epoch year на основе текущего времени в секундах
Вход: ничего
Выход: начальный epoch year
'''

import time
import datetime

sec = time.time()
now = datetime.datetime.now()
current_year = now.year

SEC_IN_COMMON_YEAR = 365*24*60*60
SEC_IN_LEAP_YEAR = 366*24*60*60


def is_leap_year(current_year):
    if current_year % 4 != 0:
        return False
    elif current_year % 100 != 0:
        return True
    elif current_year % 400 != 0:
        return False
    else:
        return True

def epoch_year(current_year, sec):
    if is_leap_year(current_year):
        sec -= SEC_IN_LEAP_YEAR
    else:
        sec -= SEC_IN_COMMON_YEAR
    current_year -= 1
    if sec > 0:
        return(epoch_year(current_year, sec))
    else:
        return(current_year+1)

epoch_year = epoch_year(current_year, sec)
print ('Epoch year is', epoch_year) 
