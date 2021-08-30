import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
import time

url = 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&sort_by=_ASC&snr=1_7_7_230_7&infinite=1'

def totalresults(url):
    r = requests.get(url)
    data = dict(r.json())
    totalresults = data['total_count']
    return int(totalresults)

def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']

def parse(data):
    gameslist = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        game_url = game.get('href')
        gameslist.append(game_url)
    return gameslist

def output(results):

    with open("games_url.csv","a",newline='') as f:
        write = csv.writer(f,dialect='excel',delimiter=';')
        write.writerows([url] for url in results)
    print('Fin. Saved to CSV')

    return

results = []
for x in range(0, totalresults(url), 100):
    data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=100&dynamic_data=&sort_by=_ASC&snr=1_7_7_230_7&infinite=1')
    output(parse(data))
    print('Results Scraped: ', x)
    time.sleep(0)

output(results)
