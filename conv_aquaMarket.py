# -*- coding: utf-8 -*-
import csv
import os
import time
import xml.etree.ElementTree as ET
import logging.config
from src.log_settings import logger_config
from src.send_emails import broken_script

logging.config.dictConfig(logger_config)

logger = logging.getLogger('')

from src.packages import download_xml, delete_csv


def write_product_csv(data, file_path):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
    with open(file, 'a', newline='') as f:
        order = ['name_product', 'cost', 'url_img', 'url_product', 'description']
        writer = csv.DictWriter(f, fieldnames=order, delimiter=';')
        writer.writerow(data)


def convert_aquaMarket(xml, FILE_PATH):
    NAME_DUBLICATE = []
    tree = ET.parse(xml)
    shop = tree.getroot()
    offers = shop[0][8]

    for item in offers:
        try:
            name_product = item.find('name').text.strip()
        except:
            name_product = ''
        try:
            cost = item.find('price').text.strip()
        except:
            cost = ''
        try:
            url_img = item.find('picture').text.strip()
        except:
            url_img = ''
        try:
            url_product = item.find('url').text
        except:
            url_product = ''
        try:
            description = item.find('description').text.strip()
        except:
            description = ''

        if name_product in NAME_DUBLICATE:
            pass
        else:
            data = {'name_product': name_product, 'cost': cost, 'url_img': url_img,
                    'url_product': url_product,
                    'description': description}
            # print(data)
            write_product_csv(data, FILE_PATH)
            NAME_DUBLICATE.append(name_product)


def download_file():
    URL = ""
    logger.info(f' - {URL}')
    download_xml(URL, '')


def main(xml, FILE_PATH):
    start = time.time()
    try:
        download_file()
        time.sleep(1)
        delete_csv(FILE_PATH)
        print('Начал конвертирвать')
        convert_aquaMarket(xml, FILE_PATH)
    except Exception as e:
        logger.error(e)
        broken_script(e, '')

    sec = (time.time() - start) / 60
    logger.info(" - {0} min.".format(round(sec, 1)))
