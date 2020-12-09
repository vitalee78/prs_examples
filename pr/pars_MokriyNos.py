import logging.config
import os
import time
from random import uniform

from src.log_settings import logger_config
from src.send_emails import email_parsing

logging.config.dictConfig(logger_config)

logger = logging.getLogger('parser_bis')

from src import packages
from src.items import Items as item


class ParsMokriyNos:
    def __init__(self):
        self.SLEEP = (uniform(0.3, 1))  # замедление парсинга, имитация поведения человека
        self.DOMEN = 'https://mokryinos.ru'
        self.file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 '//bf/prices/416075_Мокрый нос/price_MokriyNos.csv')

    def rep_product(self, s):
        return s.replace('Код товара:', '')

    def get_page_data(self, html):
        soup = packages.get_bs4(html)

        goods = soup.find('ul', id='w0').find_all('li', class_='category__item')

        for g in goods:
            url_goods = self.get_url_card(g)
            try:
                get_url = self.get_url_card(g)
                req = packages.get_fake_user_url(get_url)
                soup1 = packages.get_bs4(req)
            except Exception:
                continue
            try:
                name_goods = soup1.find('h1').text.strip()
            except Exception:
                name_goods = ''
            try:
                div = soup1.find('div', class_='product-variants').find_all('div', class_='product-variants__sku')[1].text
                id_product = div.replace('Арт. ', '')
            except Exception:
                id_product = ''
            try:
                category = soup1.find('ul', class_='breadcrumbs').find_all('li')[2].text.strip()
            except:
                category = ''
            try:
                span = soup1.find('div', class_='product-variants').find_all('span', class_='product-price')[
                    0].text.strip()
                price = span.replace(' ₽', '')
            except Exception:
                price = ''
            try:
                description = soup1.find('div', class_='product__tab-content').text.strip()
            except:
                description = ''
            try:
                url_img = self.DOMEN + soup1.find('span', class_='product-slider__item').find('img').get('src')
            except:
                url_img = ''

            data = {item.category: category, item.name_product: name_goods, item.articul: id_product,
                    item.cost: price,
                    item.url_img: url_img, item.url_product: url_goods, item.description: description}
            # print(data)
            packages.write_product_csv(data, self.file)
            # time.sleep(self.SLEEP)

    def get_url_card(self, g):
        a = g.find('div', class_='product-list-item__description').find('a').get('href')
        url_goods = self.DOMEN + a
        return url_goods

    def get_pages(self, html):
        soup = packages.get_bs4(html)
        urls = [url.text for url in soup.find('ul', class_='paging__list').find_all('a')]
        return int(urls[-1])

    def main(self, BASE_URL):
        start = time.time()
        try:
            packages.delete_csv(self.file)
            logger.debug(f'Источник - {self.DOMEN}')
            logger.info(f'Сохранил прайс \"{self.file.split("/")[-1]}\" на bf - {self.file.split("/")[4]}')
            begin_page = 1

            pages = []
            for url in BASE_URL:
                print('Открыл URL:', url)
                total_pages = self.get_pages(packages.get_fake_user_url(url))
                print('Всего найдено {} страниц...'.format(total_pages))
                for page in range(begin_page, total_pages + 1):
                    print('Собираю на странице:', page)
                    pages.append(self.get_page_data(packages.get_fake_user_url(url + "?page={}".format(page))))
        except Exception as e:
            logger.error(e)
            email_parsing(e, self.DOMEN)

        sec = (time.time() - start) / 60
        logger.info("Заняло времени: {0} min.".format(round(sec, 1)))
