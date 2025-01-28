from sqlalchemy import (Column, Integer, MetaData, String, Float, Table,
                        create_engine)
from sqlalchemy.sql import func
from databases import Database

from api.models import  RefillSchema

import os


PG_SERVER = '10.100.10.7'
PG_PORT = '5432'
PG_DB = 'billing'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'

# PG_SERVER = os.getenv("PG_SERVER")
# PG_PORT = os.getenv("PG_PORT")
# PG_DB = os.getenv("PG_DB")
# PG_USER = os.getenv("PG_USER")
# PG_PASSWORD = os.getenv("PG_PASSWORD")

DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_DB}"

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

accounts = Table(
    'accounts',
    metadata,
    Column("login", String, primary_key=True),
    Column("balance", Float, server_default='0', nullable=False),
) 

# databases query builder
database = Database(DATABASE_URL)

async def create_account(login:String):
    try:
        query = accounts.insert().values(login = login).returning(accounts.c.login, accounts.c.balance)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res


async def get_account(login:String):
    try:
        query = accounts.select().where(accounts.c.login == login)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res


async def refill(payload:RefillSchema):
    try:
        query = (accounts.update().returning( accounts.c.login, accounts.c.balance)
        ).where(accounts.c.login == payload.login).values(
            balance   =  accounts.c.balance + payload.balance)
        res = await database.fetch_one(query=query)

        if not res : return{'error': "Account not found"}
    except Exception as e:
        return {'error': str(e)}
    return res


async def withdraw(payload:RefillSchema):
    try:
        query = accounts.select().where(accounts.c.login == payload.login)
        res = await database.fetch_one(query)

        if not res:
            return {'error' : 'Account not found'}

        if (res.balance - payload.balance) < 0:
            return {'error' : 'Not enough money', "balance" : res.balance}
    except Exception as e:
        return {'error': str(e)}
    
    try:
        query = (accounts.update().returning( accounts.c.login, accounts.c.balance)
        ).where(accounts.c.login == payload.login).values(
            balance   =  accounts.c.balance - payload.balance)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res

