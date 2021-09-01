import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import time
import re
import os

basedir = os.path.abspath(os.path.dirname(__file__))
excepted_link={'out':0,'genre':0,'name':0,'lang':0}
def get_data(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def output(results):
    try:
        with open(os.path.join(basedir, 'data_game.json'), 'a') as f:
            json.dump(results, f, indent=4)
        print("Created Json File")
    except:
        excepted_link['out'] += 1
        print(excepted_link)
        pass

def parse(data):
    gamedata = {}
    gamedata['name'] = get_name(data)
    gamedata['genre_dev_date'] = get_genre_dev_date(data)
    gamedata['languages'] = get_languages(data)
    return gamedata

def get_genre_dev_date(data):
    try:
        find = data.find('div',{'id': 'genresAndManufacturer'})
        key = ''
        l = ''
        genre_dev_date = {}
        for i in find.findAll(['a','b']):    
            text = i.text
            if text == 'Title:':
                continue
            elif ':' in text:
                    genre_dev_date[key]=l
                    key = text[:-1]
                    l = []
            else:
                l.append(text)
        del genre_dev_date['']
        return genre_dev_date
    except:
        excepted_link['genre'] += 1
        print(excepted_link)
        pass

def get_languages(data):
    try:
        find = data.find('div',{'id': 'languageTable'})
        key = ''
        l = []
        languages = {'language':['Interface','Full_Audio','Subtitles']}
        for i in find.findAll('td'):
            text = i.text
            if len(text)>3:
                text = re.sub("[\\r]|[\\n]|[\\t]","",text)
                languages[key] = l
                key = text
                l = []
            elif "✔" in text:
                l.append(True)
            else:
                l.append(False)
        del languages['']
        return languages
    except:
        excepted_link['lang'] += 1
        print(excepted_link)
        pass

def get_name(data):
    try:
        find = data.find('div',{'class':'apphub_AppName'})
        return find.text
    except:
        excepted_link['name'] += 1
        print(excepted_link)
        pass

if __name__ == '__main__':
    df = pd.read_csv(os.path.join(basedir, 'games_url.csv'))
    links = list(df['url'])
    for index in range(352,len(links)):
        data = get_data(links[index])
        output(parse(data))

        print('Results Scraped: ', index)
        time.sleep(0)
    #output(results)