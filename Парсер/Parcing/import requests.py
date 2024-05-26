import requests
from bs4 import BeautifulSoup
import csv

CSV = 'tv.csv'
HOST = 'https://www.eldorado.ru/'
URL = 'https://www.eldorado.ru/c/televizory/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        tv = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу:{page}')
            html = get_html(URL, params={'page': page})
            tv.extend(get_content(html.text))
            save_doc(tv, CSV)
        print(tv)
    else:
        print('Error')

parser()