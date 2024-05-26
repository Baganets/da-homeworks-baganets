import requests
from bs4 import BeautifulSoup
import csv
import json
from selenium import webdriver
import selenium.common.exceptions as exc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time

CSV = 'tv.csv'
HOST = 'https://www.eldorado.ru/'
URL = 'https://www.eldorado.ru/c/televizory/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.headless = True
driver = webdriver.Chrome(options=options)

stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)
#Новенькое

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='wF')
    tv = []

    for item in items:
        tv.append(
            {
                'articul':item.find('a', class_='SE').get_text(),
                'title':item.find('p', class_='QE').get_text(),
                'rating':item.find('span', class_='Pp Tp').get_text(),
                'num_reviews':item.find('a', class_='VE').get_text(),
                'diag':item.find('span', class_='MD').get_text(),
                'price':item.find('span', class_='kM').get_text(),
                'price_dis':item.find('span', class_='fM pM').get_text()
            }
        )
    return tv

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Артикул', 'Название', 'Оценка', 'Количество отзывов', 'Диагональ', 'Цена', 'Цена со скидкой']) 
        for item in items:
            writer.writerow( [item['articul'], item['title'], item['rating'], item['num_reviews'], item['diag'], item['price'], item['price_dis']])

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