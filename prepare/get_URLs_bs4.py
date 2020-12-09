import csv
import os
import time

from random import uniform
from time import sleep

from src import packages

DOMEN = 'https://metrazh54.ru'


def parse(URL):
    soup = packages.get_bs4(URL)

    urls = soup.find('ul', class_='catalog_items').find_all('li', class_='catalog_item')
    for url in urls:
        cat_url = url.find('a').get('href')
        all_urls = DOMEN + cat_url
        print(all_urls)



        # data = {
        #         'urls': all_urls
        #         }
        # packages.write_csv(data)


def main():
    URL = [
        'https://metrazh54.ru/catalog/'

    ]

    pages = []
    for p in URL:
        pages.append(parse(packages.get_url_proxy(p)))


if __name__ == '__main__':
    start = time.time()
    main()
    print('---------------------------------------')
    sec = (time.time() - start) / 60
    print("Заняло времени: {0} min.".format(round(sec, 1)))
