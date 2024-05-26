import requests
from bs4 import BeautifulSoup
import csv

CSV = 'aroma.csv'
HOST = 'https://cozyhome.ru/'
URL = 'https://cozyhome.ru/aromaty'
HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ch-product-card')
    tv = []

    for item in items:
        tv.append(
            {
                'name':item.find('a', class_='product-card-link').get_text(),
                'price':item.find('strike', class_='ch-col-auto').get_text(),
                'price_dis':item.find('div', class_='ch-col-auto ch-price--old').get_text(),
                'id':item.find('a', class_='VE').get_text(),
                'rate':item.find('div', class_='ch-col-auto ch-product-card__rating').get_text(),
                'discount':item.find('div', class_='ch-product-card__bottom-inner').get_text()
            }
        )
    return tv

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Оценка', 'Оценка со скидкой', 'Артикул', 'Рейтинг', 'Скидка']) 
        for item in items:
            writer.writerow( [item['name'], item['price'], item['price_dis'], item['id'], item['rate'], item['discount']])

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