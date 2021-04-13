import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://kraskivmoskve.ru/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://kraskivmoskve.ru'
FILE = 'paints.csv'



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['link']])


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='pagination-link')
    if pagination:
        return int(pagination[-1].get_text())
    else: 
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-card-wrapper')
    
    paints = []
    for item in items:
        paints.append({
            'title': item.find('a', class_='product-link').get_text(strip=True),
            'link': HOST + item.find('a', class_='product-link').get('href')
        })
    
    return paints

def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        paints = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            paints.extend(get_content(html.text))
    else:
        print('Error!')
    save_file(paints, FILE)
    print(f'Получено { len(paints) } элементов')
    return paints

parse()
