from datetime import datetime

import requests
from bs4 import BeautifulSoup

response = requests.get(url='https://elementy.ru/novosti_nauki/433945/Endosimbioticheskaya_bakteriya_pomogaet_pochvennomu_gribku_ne_byt_sedennym_fagotsitami      ')
article_bs = BeautifulSoup(response.text, 'lxml')

date = article_bs.find('span', class_='date')
datetime_object = datetime.strptime(date.text, '%d.%m.%Y')
date_parse = datetime.strftime(datetime_object, '%Y-%m-%d %H:%M:%S')
date = date_parse
# date = datetime_object

title_bs = article_bs.find('h1')
title = title_bs.text

sublink_bs = article_bs.find('div', class_='sublink')
author_bs = sublink_bs.find('a')
author = author_bs.text

topics_bs = sublink_bs.find_all('a')[1]
topics = topics_bs.text

print(f'title is {title}\n'
      f'author is {author}\n'
      f'topics are {topics}\n'
      f'date is {date}')