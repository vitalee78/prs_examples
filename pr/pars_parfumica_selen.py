import logging.config
import time
from random import uniform
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from src.log_settings import logger_config

from src.send_emails import email_parsing

logging.config.dictConfig(logger_config)

logger = logging.getLogger('parser_bis')

from src import packages
from src.items import Items as item
from src.manager import Manager

SLEEP = (uniform(0.5, 1.5))


class ParserParfumica:
    def __init__(self, BROWSER, TOGGLE_BR):
        self.man = Manager(BROWSER, TOGGLE_BR)
        self.DOMEN = 'https://parfumica.ru'
        self.PATH_FILE = '//bf/prices/526826_Parfumica/косметика_{}.csv'.format(packages.get_date_now())

    def navigation(self):
        wd = self.man.wd
        links = [link.get_attribute("href") for link in wd.find_elements_by_xpath("//*[@class='item_info TYPE_1']//a")]

        for link in links:
            wd.get(link)
            name = wd.find_element_by_tag_name("h3").text
            try:
                cost = wd.find_element_by_xpath("//div[@class='offers_price']//span[@class='price_value']").text
            except Exception:
                cost = ''
            try:
                description = wd.find_element_by_xpath("//div[@class='detail_text']").text
            except Exception:
                description = ''
            try:
                rubric = wd.find_elements_by_xpath("//div[@id='navigation']//a[@class='number']")[-1].text
            except Exception:
                rubric = ''
            try:
                url_img = wd.find_element_by_xpath("//div[@class='slides']//img").get_attribute("src")
            except Exception:
                url_img = ''

            data = {
                item.category: rubric,
                item.name_product: name,
                item.cost: cost,
                item.description: description,
                item.url_img: url_img,
                item.url_product: link
            }
            print(data)
            sleep(SLEEP)
            packages.write_product_csv(data, self.PATH_FILE)
            wd.back()

    def pagination(self):
        wd = self.man.wd
        pages = wd.find_elements_by_xpath("//div[@class='nums']//a")[-1].text
        return int(pages)

    # def get_urls(self, html):
    #     URLS = []
    #     soup = packages.get_bs4(html)
    #     table = soup.find('ul', class_='menu dropdown').find_all('li', class_='full')
    #     for t in table:
    #         cat_url = t.find('a').get('href')
    #         www = self.DOMEN + cat_url
    #         URLS.append(www)
    #     return URLS

    def main(self, URLS):
        wd = self.man.wd
        start = time.time()
        try:
            logger.debug(f'Источник - {self.DOMEN}')
            logger.info(f'Сохранил прайс \"{self.PATH_FILE.split("/")[-1]}\" на bf - {self.PATH_FILE.split("/")[4]}')
            logger.info('Собирал через браузер Chrome')
            # urls = self.get_urls(packages.get_fake_user_url(BASE_URL))

            for url in URLS:
                print(f'Scraping in {url}')

                self.man.get_html(url)
                count_pages = self.pagination()
                print(f'Всего страниц: {count_pages}')
                self.navigation()

                for page in range(2, count_pages + 1):
                    print(f'Собираю на странице: {page}')
                    try:
                        wd.find_element_by_xpath(f"//div[@class='nums']//a[text()='{page}']").click()
                        time.sleep(2)
                        self.navigation()
                    except NoSuchElementException:
                        pass
        except Exception as e:
            email_parsing(e, self.DOMEN)
            logger.error(e)

        sec = (time.time() - start) / 60
        logger.info("Заняло времени: {0} min.".format(round(sec, 1)))

        self.man.destroy()
