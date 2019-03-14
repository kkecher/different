'''
IN PROGRESS!
'''

from bs4 import BeautifulSoup as bs
import urllib.request
import re

#dir_url = input('Enter dir_url: ')
dir_url = 'https://www.farpost.ru/sport/'
source = urllib.request.urlopen(dir_url)
soup = bs(source, 'html.parser')
#print(soup.prettify())
#print(soup.title) #<title>Моторное и трансмиссионное масло купить ! Цены. Выбор.</title>
#print(soup.title.name)
#print(soup.title.string)
#for link in soup.find_all('title'):
#    print(link.get('href'))
#for text in soup.get_text():
#    print(text)
divs = (soup.find_all('a'))
#for div in divs:
#    for child in div.descendants:
#        print(child)
#        print()
#        print('################')
#        print()
#for string in soup.strings:
#    print(repr(string))
#htmls = soup.find_all(tag.has_attr('class'))
#def has_class_but_no_id(tag):
#    return tag.has_attr('class')
#soup.find_all(has_class_but_no_id)
#for line in soup:
#    print(line)
#    if 'title' in line:
#        print(line)
#        print()
#        print('##################')
#        print()
#
#soup.find_all(re.compile('title').search('class'))
#for line in soup:
#    print(line)
#    print()
#    input('Next…')
#    print()
#test = soup.find_all('a', class_='bulletinLink')
#for line in test:
#    print(line.find('a').get_text())
#print(test)
#print(len(test))
#for line in test:
#    print(line)
#    input('Next...')
#test = soup.find_all('a', class_='bulletinLink') + soup.find_all('div', class_='title')
#flag = 0
#for line in test:
#    if flag==0:
#        next
#    flag = 1
#    print(line.text)
#print(len(test)-1)


#test = soup.find_all('div', 'text')
#for line in test:
#    print(line.)

test = soup.select(['.title','.bulletinLink'])
for i in test:
    print(i)
