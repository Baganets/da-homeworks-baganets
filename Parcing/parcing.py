from bs4 import BeautifulSoup
import csv
import requests
import openpyxl
import pandas as pd
import xlsxwriter
import sqlite3
import re

HOST = 'https://cozyhome.ru/'
URL = 'https://cozyhome.ru/aromaty'
HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text

product_id_1 = 1
product_id_2 = 1

def get_content(html):
    global product_id_1, product_id_2
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="ch-product-card")
    Aromati1 = []
    Aromati2 = []
    for item in items:
        try:
            price = item.find('strike', class_='ch-col-auto').get_text().strip().replace(' ', '')
            price_dis = item.find('div', class_='ch-col-auto').get_text().strip().replace(' ', '')

            if item.find('div', class_='ch-product-card__bottom-inner').get_text().strip():
                Aromati1.append({
                    'id': product_id_1,
                    'name': item.find('div', class_='ch-product-card__title').get_text().strip(),
                    'price': price,
                    'price_dis': price_dis,
                    'rate': item.find('div', class_='ch-product-card__rating').get_text().strip(),
                    'discount': item.find('div', class_='ch-product-card__bottom-inner').get_text().strip(),
                })
                product_id_1 += 1

            item_title = item.find('div', class_='ch-product-card__title').get_text()
            extra_type = re.search(r'Диффузор|Свеча ароматическая|Набор ароматический|Саше|Набор свечей|Свеча', item_title)
            if extra_type:
                Aromati2.append({
                        'id': product_id_2,
                        'type': extra_type.group(),
                })
                product_id_2 += 1
        except AttributeError:
            continue
    return Aromati1, Aromati2  

def save_to_sqlite(Aromati1, Aromati2):
    conn = sqlite3.connect('D:/games/homework/da-homeworks-baganets/Parcing/Aromati.db')
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS Aromati1")
    c.execute("DROP TABLE IF EXISTS Aromati2")

    c.execute('''CREATE TABLE IF NOT EXISTS Aromati1
                 (id INTEGER PRIMARY KEY, name TEXT, price TEXT, price_dis TEXT, rate TEXT, discount TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Aromati2
                 (id INTEGER PRIMARY KEY, type TEXT)''')

    for item in Aromati1:
        c.execute("INSERT INTO Aromati1 VALUES (?, ?, ?, ?, ?, ?)",
                  (item['id'], item['name'], item['price'], item['price_dis'], item['rate'], item['discount']))

    for item in Aromati2:
        c.execute("INSERT INTO Aromati2 VALUES (?, ?)",
                  (item['id'], item['type']))

    conn.commit()
    conn.close()

def parser():
    PAGINATION = int(input('Укажите количество страниц для парсинга: '))
    html = get_html(URL)
    if html:
        Aromati1 = []
        Aromati2 = []
        for page in range(1, PAGINATION + 1):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'PAGEN_1': page})
            data1, data2 = get_content(html)
            Aromati1.extend(data1)
            Aromati2.extend(data2)
        
        save_to_sqlite(Aromati1, Aromati2)
        
        print('Данные успешно сохранены в базу данных!')
    else:
        print('Произошла ошибка при получении HTML')

parser()
