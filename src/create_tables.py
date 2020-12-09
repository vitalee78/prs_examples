import csv
import datetime
import configparser

from peewee import *



MYSQL = 'mysql_test'

FILE_NAME = '../csv/calendar.csv'

config = configparser.ConfigParser()
config.read('../config.ini', encoding='utf-8-sig')
dbhandle = MySQLDatabase(host=config.get(MYSQL, 'host'),
                         database=config.get(MYSQL, 'database'),
                         user=config.get(MYSQL, 'user'),
                         password=config.get(MYSQL, 'password'))


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Data_Beton(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField()
    price = IntegerField(null=True)
    params = CharField()
    url_img = TextField()
    url = TextField()
    created_date = DateTimeField(default=datetime.datetime.now())
    updated_date = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'pars_beton_nsk'


class Bis_Workdays(BaseModel):
    date = DateTimeField()

    class Meta:
        db_table = 'calendar'


# для наполнения данными в таблицу из csv файла
def push_db():
    # dbhandle.connect()
    # dbhandle.create_tables([Data_Beton])

    with open(FILE_NAME) as f:
        order = ['date']
        reader = csv.DictReader(f, fieldnames=order, delimiter=';')

        push = list(reader)

        with dbhandle.atomic():
            for row in push:
                Bis_Workdays.create(**row)


if __name__ == '__main__':
    push_db()
    # try:
    #     dbhandle.connect()
    #     Data_Beton.create_table()
    # except InternalError as e:
    #     print(str(e))
