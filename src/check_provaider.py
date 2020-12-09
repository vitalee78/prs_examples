from random import choice

from src import packages


'''
    Для проверки замены прокси и user-agent на сайте http://sitespy.ru/my-ip
    Скрипт должен выводить, произвольно, разные ip:port и user-agent 
'''

def get_ip(html):
    soup = packages.get_bs4(html)

    ip = soup.find('span', class_='ip').text.split()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.split()
    print(ip, ua)
    print('--------------------------------')


# def get_html(url):
#     # proxies = {'https': 'ipaddress:5000'}
#     p = get_proxy() # {'schema': '', 'address': ''}
#
#     proxy = {p['schema']: p['address'] }
#     r = requests.get(url, proxies=proxy, timeout=5)
#     return r.json()
def read_files():
    useragents = open('../data/useragents.txt').read().split('\n')
    proxies = open('../data/proxies.txt').read().split('\n')

    for i in range(10):
        proxy = {'schema': choice(proxies)}
        # print(proxy)
        useragent = {'User-Agent': choice(useragents)}
        # print(useragent)
        return proxy, useragent

def main():
    url = 'http://sitespy.ru/my-ip'

    html = packages.get_url(url)
    get_ip(html)

if __name__ == '__main__':
    main()
