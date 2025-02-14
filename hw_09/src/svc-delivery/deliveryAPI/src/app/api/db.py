from sqlalchemy import (Column, Integer, MetaData, String, Float, Table, DateTime,
                        create_engine)
from sqlalchemy.sql import func, text
from databases import Database

from api.models import  DeliverySchema

import os


PG_SERVER = '10.100.10.7'
PG_PORT = '5432'
PG_DB = 'delivery'
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

delivery = Table(
    'delivery',
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_order", Integer),
    Column("dtime", DateTime),
) 

# databases query builder
database = Database(DATABASE_URL)


async def get_delivery_pool():
    try:
        query = delivery.select()
        res = await database.fetch_all(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res


async def reserve_delivery(payload:DeliverySchema):
    sql = text(f"""SELECT
                ( coalesce((SELECT dtime FROM delivery where dtime >= '{payload.dtime}' order by dtime  limit 1),'2999-01-01 00:00:00')
                                                                    - '{payload.dtime}'
                )  >= '1 hour'::interval
            and
                (                                                   '{payload.dtime}' -
                coalesce((SELECT dtime FROM delivery where dtime <= '{payload.dtime}' order by dtime desc limit 1), '1999-01-01 00:00:00')
                    >= '1 hour'::interval) 
            as is_avail""")
    
    try:
        res =  await database.execute(sql)
    except Exception as e:
        res = str(e)
    
    if not res:
        return {"error": "Not empty time slot"}
    
    try:
        query = delivery.insert().values(id_order  = payload.id_order,
                                         dtime = payload.dtime).returning(delivery.c.id)
        res = await database.fetch_one(query=query)
    except Exception as e:
        return {'error': str(e)}
    return res
    



