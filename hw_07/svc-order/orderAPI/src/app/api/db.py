

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Float, Table,
                        create_engine)
from sqlalchemy.sql import func
from databases import Database
from datetime import datetime

from api.models import  OrderSchema

import os


# PG_SERVER = '10.100.10.7'
# PG_PORT = '5432'
# PG_DB = 'order'
# PG_USER = 'postgres'
# PG_PASSWORD = 'postgres'

PG_SERVER = os.getenv("PG_SERVER")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_DB}"

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()


orders = Table(
    'orders',
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("login", String),
    Column("e_mail", String),
    Column("id_cart", Integer, server_default='0', nullable=False),
    Column("amount", Float, server_default='0', nullable=False),
    Column("status", Integer, server_default='0', nullable=False),
    Column("dtime", DateTime, default=datetime.now()),
) 

# databases query builder
database = Database(DATABASE_URL)

async def create_order(payload:OrderSchema, order_status:int):
    try:
        query = orders.insert().values(login = payload.login
                                       ,e_mail = payload.e_mail
                                       ,amount = payload.amount
                                       ,id_cart = payload.id_cart
                                       ,status = order_status
                                       ,dtime = datetime.now()).returning(orders.c.id, orders.c.status)
        
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res


# async def get_account(login:String):
#     try:
#         query = accounts.select().where(accounts.c.login == login)
#         res = await database.fetch_one(query=query)
#     except Exception as e:
#         return {'error': str(e)}
#     return res


# async def refill(payload:RefillSchema):
#     try:
#         query = (accounts.update().returning( accounts.c.login, accounts.c.balance)
#         ).where(accounts.c.login == payload.login).values(
#             balance   =  accounts.c.balance + payload.balance)
#         res = await database.fetch_one(query=query)

#         if not res : return{'error': "Account not found"}
#     except Exception as e:
#         return {'error': str(e)}
#     return res


# async def withdraw(payload:RefillSchema):
#     try:
#         query = accounts.select().where(accounts.c.login == payload.login)
#         res = await database.fetch_one(query)
        
#         if (res.balance - payload.balance) < 0:
#             return {'error' : 'not enough money in the account', "balance" : res.balance}
#     except Exception as e:
#         return {'error': str(e)}

#     try:
#         query = (accounts.update().returning( accounts.c.login, accounts.c.balance)
#         ).where(accounts.c.login == payload.login).values(
#             balance   =  accounts.c.balance - payload.balance)
#         res = await database.fetch_one(query=query)
#         # res1 = res.fetchall()
#     except Exception as e:
#         return {'error': str(e)}
#     return res #{"login": payload.login,"balance": res}


