import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy import text
from sqlalchemy.sql import func
from databases import Database

from api.models import UserSchema


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
    Column("id", Integer, primary_key=True),
    Column("login", String, unique=True),
    Column("first_name", String),
    Column("last_name", String), 
    Column("email", String, unique=True),
    Column("age", Integer),
    Column("phone", String, unique=True)
)

# databases query builder
database = Database(DATABASE_URL)

async def select_by_id(id):
    query = users.select().where(id == users.c.id)
    return  await database.fetch_one(query=query) or f'User whith id={id} is not exists' 

async def select_all():
    query = users.select()
    return await database.fetch_all(query=query)

async def insert(payload:UserSchema):
    query = users.insert().values(
        login       = payload.login,
        first_name  = payload.first_name,
        middle_name = payload.middle_name,
        last_name   = payload.last_name,
        age         = payload.age,
        phone       = payload.phone,
        email       = payload.email 
    ).returning(users.c.id)
    return await database.execute(query=query)


async def update(id:int, payload:UserSchema):
    sql = text(f"""INSERT INTO users(id, login, first_name, last_name, email, age, phone) 
               VALUES  ({id},'{payload.login}','{payload.first_name}','{payload.last_name}','{ payload.email }',{payload.age}, '{payload.phone}')
               ON CONFLICT (id) DO UPDATE
               SET
                    age = EXCLUDED.age,
                    phone = EXCLUDED.phone,
                    email = EXCLUDED.email""")
    
    try:
        res =  await database.execute(sql)
    except Exception as e:
        res = str(e)

    return res
    
    query = users.update().where(id == users.c.id).values(
        login       = payload.login,
        first_name  = payload.first_name,
        middle_name = payload.middle_name,
        last_name   = payload.last_name,
        age         = payload.age,
        phone       = payload.phone,
        email       = payload.email 
    ).returning(users.c.id)
    return await database.execute(query=query)


async def delete(id):
    query = users.delete().where(id == users.c.id)
    return  await database.fetch_one(query=query)