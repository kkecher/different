'''
Собирает все URL'ы из sitemap'ов
Вход: URL в sitemap'ами
Выход: Файл с URL'ами из sitemap'а
'''

import urllib.request
import re

url = input('Enter sitemap ULR: ')
result = input('Enter result file: ')

url_list = []
def get_urls(url):
    '''
    Собирает все URL'ы из sitemap'ов
    Вход: URL в sitemap'ами
    Выход: список с URL'ами из sitemap'а
    '''
    url_list_temp = []
    source = urllib.request.urlopen(url)
    for line in source:
        url_list_temp += re.findall('<loc>(.*?)<\/loc>', line.decode('cp1251'))
    for url in url_list_temp:
        try:
            if '.xml' in url:
                print(url + ' — we need to go deeper!')
                get_urls(url)
            else:
                url_list.append(url)
        except:
            continue
    return(url_list)

url_list = get_urls(url)

with open(result, 'w') as f:
    for url in url_list:
        f.write(url + '\n')
