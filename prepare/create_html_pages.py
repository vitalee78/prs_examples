import requests
from pathlib import Path

'''
    Предназначен для загрузки страниц html в локальную папку `csv` проекта,
    для отладки в оффлайне
'''


BASE_URL = 'https://abakan.orgdir.ru/shinnyy-dvor-sovetskaya-c9711414977496636/?h=Fkrvp749G45545AA75IGGGGankztzs59G6G7G7I2G12H1J87qpgm3A7I5758G99117079JG3oxEhuv8A5688A6759I9AH5J51'
BASE_PATH = Path('./html')

for i in range(1, 2):
    r = requests.get(BASE_URL.format(page_num=i))

    print(r.status_code)

    html_file_path = BASE_PATH / 'orgdir_card{page_num}.html'.format(page_num=i)

    with open(str(html_file_path), 'wb') as f:
        f.write(r.content)

