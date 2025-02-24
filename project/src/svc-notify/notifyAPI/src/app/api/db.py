

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Boolean, Table,
                        create_engine, exc, desc)
from sqlalchemy.sql import func
from databases import Database

from api.models import MessageSchema
from datetime import datetime
import os


# PG_SERVER = '10.100.10.7'
# PG_PORT = '5432'
# PG_DB = 'notify'
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


message_log = Table(
    'message_log',
    metadata,
    Column("id", Integer, primary_key=True,autoincrement=True),
    Column("login", String),
    Column("email", String),
    Column("dtime", DateTime, default=datetime.now()),
    Column("text", String),
    Column("is_sended", Boolean),
) 

# databases query builder
database = Database(DATABASE_URL)

async def log_message(payload:MessageSchema, is_sended):
    try:
        query = message_log.insert().values(
            login       = payload.login,
            email       = payload.e_mail,
            text        = payload.text,
            dtime       = datetime.now(),
            is_sended   = is_sended
        ).returning(message_log.c.id, message_log.c.is_sended)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res



async def get_message_log(login):
    query = message_log.select().where(login == message_log.c.login)
    messages = await database.fetch_all(query=query)
    return messages



async def get_message(id):
    query = message_log.select().where(id == message_log.c.id)
    message = await database.fetch_one(query=query)

    return message