import datetime

from peewee import *
from config import config

Mysql = 'db'

db = config[Mysql]
dbhandle = MySQLDatabase(host=db['host'],
                         database=db['database'],
                         user=db['user'],
                         password=db['pass'])

class BaseModel(Model):
    class Meta:
        database = dbhandle


class Data_Avito(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField()
    price = IntegerField(null=True)
    period = CharField()
    param = CharField()
    url = TextField()
    created_date = DateTimeField(default=datetime.datetime.now())
    updated_date = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = ''

def select_count():
    query = Data_Avito.select(Data_Avito.id).count()
    return query

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
        db_table = ''


class Data_Cities(BaseModel):
    id_city = PrimaryKeyField(null=False)
    name_city = CharField()
    trans = CharField(null=True)
    active = IntegerField()

    class Meta:
        db_table = ''


def select_city_trans():
    for item in Data_Cities.select():
        print(item.name_city, item.trans)

if __name__ == '__main__':
    select_city_trans()

# вставка данных в таблицу БД MySql
# def insert_db(data):
#     try:
#         with dbhandle.transaction():
#             Data_Beton.insert_many(data).execute()
#     except IntegrityError as e:
#         print(e)
#         dbhandle.rollback()

