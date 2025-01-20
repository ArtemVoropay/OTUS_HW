

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, exc)
from sqlalchemy.sql import func
from databases import Database

from api.models import UserSchema, AuthData
import os


# PG_SERVER = '10.100.10.7'
# PG_PORT = '5432'
# PG_DB = 'users'
# PG_USER = 'postgres'
# PG_PASSWORD = 'postgres'

PG_SERVER = os.getenv("PG_SERVER")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_DB}"

# DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = ("postgresql+psycopg2://postgres:postgres@10.100.10.7:5432/users")


# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column("id", Integer, primary_key=True,autoincrement=True),
    Column("login", String, unique=True),
    Column("first_name", String),
    Column("last_name", String), 
    Column("email", String, unique=True),
    Column("password", String),
) 

# databases query builder
database = Database(DATABASE_URL)

async def register(payload:UserSchema):
    try:
        query = users.insert().values(
            login       = payload.login,
            first_name  = payload.first_name,
            last_name   = payload.last_name,
            email       = payload.email,
            password    = payload.password
        ).returning(users.c.id)
        res = await database.execute(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res


async def login(payload:AuthData):
    query = users.select().where(payload.login == users.c.login)
    user = await database.fetch_one(query=query)
    if not user:
        return None
    if user.password != payload.password:
        return 'password incorrect'
    return  user or None
