import datetime
import os
import time
from multiprocessing.pool import Pool
from colorama import init, Fore

from src.send_emails import email_checking, broken_script
from src.send_sms import SMSC

init()
directories = [
    

]
date_now = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
smsc = SMSC()


def get_folders(directory):
    count = []
    path = os.walk(directory)
    for folder in path:
        create_folders = datetime.datetime.fromtimestamp(os.path.getctime(folder[0]))
        datetime_now = datetime.datetime.strftime(create_folders, "%d-%m-%Y %H:%M")
        if datetime_now == date_now:
            count.append(folder[0])
            print(Fore.RED + f'Подозрительные движение {folder[0]}')
            if len(count) > 10:
                break
    if len(count) > 10:
        print(f'Подозрительное движение в папках - {count}')
        smsc.send_sms("Подозрительное движение в папках на BF, подробности на эл. ящике", sender="sms BIS")
        email_checking(count)


def streams(paths):
    get_folders(paths)


if __name__ == '__main__':
    print(Fore.GREEN + 'Начал проверку папок на BF, на наличие вируса-шифровальщика.')
    try:
        start = time.time()
        Pool(10).map(streams, directories)
        sec = (time.time() - start) / 60
        print("Заняло времени: {0} min.".format(round(sec, 1)))
    except Exception as e:
        broken_script(e, 'Проверка на вирус шифрования')
