import re
import os
import csv
import time
import urllib

from random import uniform
from time import sleep
from urllib.request import urlopen

from src import packages

'''
    Для проверки замены прокси и user-agent на сайте http://sitespy.ru/my-ip
    Скрипт должен выводить, произвольно, разные ip:port и user-agent 
'''

URL = 'http://sitespy.ru/my-ip'

def parse():
    html = packages.get_urllib(URL)

    # response = urllib.request.urlopen(URL)
    # html = response.read().decode('utf-8', errors='ignore')

    ip = re.findall('<span class="ip">(.+?)</span>', html)
    useragent = re.findall('<strong>User-Agent:</strong>(.+?)</span>', html)
    print(ip, useragent)


if __name__ == '__main__':
    parse()