# -*- coding: utf-8 -*-
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import config

today = datetime.date.today().strftime("%d-%m-%Y")
email_ = config['mail']
MAIL_SERVER = email_['server']
FROM_EMAIL = email_['from']
EMAIL_TO = email_['to']
FROM_ = '{email}'.format(email=FROM_EMAIL)

mail = smtplib.SMTP()
mail.connect(MAIL_SERVER, 25)
mail.ehlo()


def mail_sendmail(msg, text_body):
    part = MIMEText(text_body, 'html')
    msg.attach(part)
    mail.sendmail(FROM_EMAIL, EMAIL_TO, msg.as_string())
    mail.quit()


def email_parsing(error, source):
    template = '''<!doctype html><html lang="en">
                    <head><meta charset="utf-8"></head>
                    <body>'''
    content = '''<h4>Данные об источнике.</h4><hr>'''
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f' {source}  {today}'
    msg['From'] = FROM_
    content += '<p><font color="red" face="Arial">{}</font></p>'.format(f' - {error}')
    content += '<p>{}</p>'.format(f'Источник {source}')
    # content += '<p>{}</p>'.format(f'Код фирмы на bf - {file.split("/")[4]}')
    content += '''<h4><hr>Письмо отправлено автоматически для оповещения менеджеров, 
                    на всякий случай сообщите в IT отдел, вдруг не в курсе... Спасибо!
                                <h4><br/>'''
    end = '</body></html>'
    text_body = template + content + end
    mail_sendmail(msg, text_body)


def email_checking(folders):
    template = '''<!doctype html><html lang="en">
                    <head><meta charset="utf-8"></head>
                    <body>'''
    content = '''<h4>Возможно шифрование файлов вирусом!</h4><hr>'''
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f' {today}'
    msg['From'] = FROM_
    content += '<p>{}</p>'.format(f'Папки на BF {folders}')
    content += '<p>{}</p>'.format(
        '')
    content += '''<h4><hr>Необходимо проверить в папках файлы на наличие шифрования, может действовать вирус!  
                                <h4><br/>'''
    end = '</body></html>'
    text_body = template + content + end
    mail_sendmail(msg, text_body)


def broken_script(error, script_name):
    template = '''<!doctype html><html lang="en">
                    <head><meta charset="utf-8"></head>
                    <body>'''
    content = '''<h4>Нужно узнать причину, почему не отработал скрипт.</h4><hr>'''
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Сломался скрипт - "{script_name}", дата - {today}'
    msg['From'] = FROM_
    content += '<p><font color="red" face="Arial">{}</font></p>'.format(f' - {error}')
    content += '''<h4><hr>Скрипт запускается через планировщик задач на сервере 192.168.0.13 (vitaliy.li, 123456780), находится в F:\Projects_077\parsersBis\   
                                <h4><br/>'''
    end = '</body></html>'
    text_body = template + content + end
    mail_sendmail(msg, text_body)
