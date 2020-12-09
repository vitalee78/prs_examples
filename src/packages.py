# -*- coding: utf-8 -*-
import requests
import csv
import glob
import os
import shutil
import urllib
import socket
import json

from datetime import datetime, timedelta
from random import choice
from bs4 import BeautifulSoup
from urllib.request import urlopen
from fake_useragent import UserAgent
from multiprocessing import Pool

from src.log_settings import logger_config
import logging.config

from src.send_emails import email_parsing

logging.config.dictConfig(logger_config)

logger = logging.getLogger('')

'''
    Методы и функции для парсеров, чтобы не дублировать код, пакеты, библиотеки 
'''

file_users = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/useragents.txt')
file_proxies_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/proxies.json')
file_proxies = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/urls.csv')


# функция для подключения к сайту с заменой прокси и User-Agent
def get_url_proxy(url, proxy=None):
    # useragents = open(file_users).read().split('\n')
    proxies = open(file_proxies).read().split('\n')

    for i in range(48):
        proxy = {'schema': choice(proxies)}
        # useragent = {'User-Agent': choice(useragents)}
    r = requests.get(url, headers={'User-Agent': UserAgent().random}, proxies=proxy)

    if r.ok:
        return r.text
    logger.error(f'Ошибка подключения к сайту - {r.status_code}')


# функция для подключения к сайту c постоянным прокси и заменой User-Agent, вариант - 2
def get_fake_user_url(url):
    ''' safari chrome ff ie msie google random'''
    r = requests.get(url, headers={'User-Agent': UserAgent().random})

    if r.status_code == 410:
        return r.text
    elif r.ok:
        return r.text
    logger.error(f'Ошибка подключения к сайту - {r.status_code}')


# функция для подключения к сайту с заменой прокси и User-Agent для парсинга регулярными вырожениями
def get_urllib(url):
    # timeout = 20
    # try:
    #     socket.setdefaulttimeout(timeout)
    # except Exception:
    #     pass

    with open(file_proxies_json) as proxies:
        proxy = json.load(proxies)
        proxy_support = urllib.request.ProxyHandler(proxy)
        try:
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
        except socket.error:
            pass
        except ConnectionResetError:
            pass
        except Exception:
            pass

    request = urllib.request.Request(url, headers={'User-Agent': UserAgent().random})
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8', errors='ignore')

    # for key, value in request.headers.items():
    #     print(key + ": " + value)
    return html


# функция для подключения к сайту c постоянным прокси и заменой User-Agent
def get_url(url, useragent=None):
    useragents = open('../data/useragents.txt').read().split('\n')
    for i in range(76):
        useragent = {'User-Agent': choice(useragents)}
    r = requests.get(url, headers=useragent)

    if r.ok:
        return r.text
    logger.error(f'Ошибка подключения к сайту - {r.status_code}')


# для подключения к модулю BeautifulSoup
def get_bs4(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


# функция для записи файла с прокси, с разных источников
def write_csv(data):
    FILE_NAME = '../data/urls.csv'

    with open(FILE_NAME, 'a', newline='') as f:
        order = ['schema']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)

    return data


# Удаляю файл
def delete_csv(myfile):
    try:
        os.remove(myfile)
    except OSError:
        pass
    else:
        print("Старый прайс удалён!")
    return myfile


# получить текущею дату для подстановки в название файла
def get_date_now():
    date_format = '%d%m%Y'
    today = datetime.now()
    return today.strftime(date_format)


def get_xml(url):
    return urlopen(url)


def get_urllib2(url):
    request = urllib.request.Request(url, headers={'User-Agent': UserAgent().random})
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8', errors='ignore')

    # for key, value in request.headers.items():
    #     print(key + ": " + value)
    #
    return html


def write_product_csv(data, FILE_PATH):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILE_PATH)
    with open(file, 'a+', newline='', errors='ignore') as f:
        order = ['articul', 'category', 'name_product', 'properties', 'cost', 'url_img', 'url_product', 'description']
        writer = csv.DictWriter(f, fieldnames=order, delimiter=';')
        writer.writerow(data)


def get_urls(html, domen, ul_tag, li_tag, locator):
    URLS = []
    soup = get_bs4(html)
    urls = soup.find(ul_tag, class_=locator).find_all(li_tag)
    for url in urls:
        cat_url = url.find('a').get('href')
        if cat_url == '':
            pass
        else:
            www = domen + cat_url
            URLS.append(www)
    return URLS


def download_xml(url, name_file):
    xml = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../xml/{name_file}')
    response = requests.get(url)
    with open(xml, 'wb') as file:
        file.write(response.content)


def get_threads(threads, func, urls):
    with Pool(threads) as p:
        p.map(func, urls)


def toggle_delete_file(condition, path):
    '''
        Чтобы не копились файлы, перед сбором новых дынных
        удаляем старый прайс-лист
    :param condition: условия 'on' - файл удалиться, 'off' файл останется пержним, данные будут добавляться в конец файла
    :param path:
    '''
    if condition == 'on':
        delete_csv(path)
    pass

def check_site(html, tag, locator, DOMEN):
    '''
        Проверка доступности сайта, если не работает, то уходит сообщение на эл. ящик
    :param DOMEN:
    :param tag:
    :param locator:
    :return:
    '''
    soup = get_bs4(html)
    logo_company = soup.find(tag, locator)
    if logo_company:
        pass
    else:
        email_parsing(f'Сайт не доступен', DOMEN)