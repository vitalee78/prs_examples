import re
import os
import csv
import time

from random import uniform
from time import sleep

from src import packages


SLEEP = (uniform(1, 2))
DOMEN = 'http://sportmag52.ru'


def write_csv(data):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '//bf/prices/241_спорт/utls {}.csv'.format(packages.get_date_now()))
    try:
        with open(file, 'a', newline='') as f:
            order = ['url']
            writer = csv.DictWriter(f, fieldnames=order, delimiter=';')
            writer.writerow(data)
    except Exception:
        pass

def parse(html):
    get_card = re.findall('item iblock section_item_inner">', html)
    print(get_card)
    # print(len(get_card[1:]))
    # get_price = re.findall('<div class="minPrice"><span>(.+?)</span>', html)
    # print(len(get_price))
    #
    # get_urls = re.findall('<a href="(.+?)" title="(.+?)">', html)
    #
    # for url in get_urls[1:]:
    #     data = []
    #     get_url = DOMEN + url[0]
    #     data.append(get_url)

        # write_csv(data)

def main():
    URL = 'http://www.krepeg.net/catalog/'

    pages = []
    for p in URL:
        print('Открыл URL:', p)
        pages.append(parse(packages.get_urllib2(p)))


if __name__ == '__main__':
    start = time.time()
    main()
    print('---------------------------------------')
    sec = ((time.time() - start)) / 60
    print("Заняло времени: {0} min.".format(round(sec, 1)))