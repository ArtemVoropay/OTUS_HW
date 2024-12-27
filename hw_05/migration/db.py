import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.sql import func
from databases import Database




PG_SERVER = os.getenv("PG_SERVER")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_DB}"


# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column("id", Integer, primary_key=True,autoincrement=True),
    Column("login", String, unique=True),
    Column("first_name", String),
    Column("middle_name", String),
    Column("last_name", String), 
    Column("age", Integer),
    Column("phone", String, unique=True), 
    Column("email", String, unique=True)
)

# databases query builder
database = Database(DATABASE_URL)


