from sqlalchemy import (Column, Integer, MetaData, String, Float, Table, 
                        create_engine)
from sqlalchemy.sql import func, text
from databases import Database

from api.models import  StockSchema, StockMoveSchema

import os


# PG_SERVER = '10.100.10.7'
# PG_PORT = '5432'
# PG_DB = 'stock'
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

stock = Table(
    'stock',
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String, nullable=False),
    Column("quantity", Integer, nullable=False),
    
) 

# databases query builder
database = Database(DATABASE_URL)




async def create_position(payload:StockSchema):
    try:
        query = stock.insert().values(description = payload.description, quantity = payload.quantity).returning(stock.c.id)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res


async def get_all_products():
    try:
        query = stock.select()
        res = await database.fetch_all(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res


async def get_product(id:int):
    try:
        query = stock.select().where(stock.c.id == id)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res



async def withdraw(payload:StockMoveSchema):
    try:
        query = stock.select().where(stock.c.id == payload.id)
        res = await database.fetch_one(query)

        if not res:
            return {'error' : 'Position not found'}

        if (res.quantity - payload.quantity) < 0:
            return {'error' : 'Not enough position quantity', "quantity" : res.quantity}
    except Exception as e:
        return {'error': str(e)}
    
    try:
        query = (stock.update().returning( stock.c.description, stock.c.description, stock.c.quantity)
        ).where(stock.c.id == payload.id).values(
            quantity   =  stock.c.quantity - payload.quantity)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return {'status':'Success reserved'}



async def refill(payload:StockMoveSchema):
    try:
        query = (stock.update().returning( stock.c.id, stock.c.description, stock.c.quantity)
        ).where(stock.c.id == payload.id).values(
            quantity   =  stock.c.quantity + payload.quantity)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
   
    return res

