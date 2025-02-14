

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Float, Table, text,
                        create_engine)
from sqlalchemy.sql import func, desc
from databases import Database
from datetime import datetime

from api.models import  OrderSchema
from api.rpc import publish

import os


PG_SERVER = '10.100.10.7'
PG_PORT = '5432'
PG_DB = 'order'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'

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
    Column("id_product", Integer, server_default='0', nullable=False),
    Column("quantity", Integer, server_default='0', nullable=False),
    Column("amount", Float, server_default='0', nullable=False),
    Column("status", String),
    Column("dtime", DateTime, default=datetime.now()),
    Column("request_id", String, nullable=False)
) 

# databases query builder
database = Database(DATABASE_URL)

async def create_order(payload:OrderSchema, order_status:str, request_id:str):
    query = orders.select().where(orders.c.request_id == request_id)
    res = await database.fetch_one(query=query)
    if res:
        return {'error': 'Request already exists'}
    try:
        query = orders.insert().values(login = payload.login
                                       ,e_mail = payload.e_mail
                                       ,amount = payload.amount
                                       ,id_product = payload.id_product
                                       ,quantity = payload.quntity
                                       ,status = order_status
                                       ,dtime = payload.dtime
                                       ,request_id = request_id).returning(orders.c.id, orders.c.login,  orders.c.amount, orders.c.request_id)
        
        res = await database.fetch_one(query=query)

    except Exception as e:
        return {'error': str(e)}
    return res


async def get_order(id:int):
    try:
        query = orders.select().where(orders.c.id == id)
        
        res = await database.fetch_one(query=query)

    except Exception as e:
        return {'error': str(e)}
    return res


async def get_last_order():
    try:
        query = orders.select().order_by(desc(orders.c.id))
        
        res = await database.fetch_one(query=query)

    except Exception as e:
        return {'error': str(e)}
    return res



async def set_order_status(id:int, order_status:str):
    query = orders.update().returning(orders.c.id, orders.c.login,  orders.c.amount,  orders.c.status
                                    ).where(orders.c.id == id
                                    ).values(status = order_status)
    res = await database.fetch_one(query)

    if not res:
        print(f'ORDER NOT FOUND (id = {id})')
        return None
    print(f"SET ORDER STATUS: id:{res['id']}  status:{res['status']}") 
    return res

