
import logging
from fastapi import FastAPI, Query, Request
from typing import Optional
from api import users
from api import health
from api.db import engine, metadata, database

metadata.create_all(engine)



#uvicorn main:app --reload --host 0.0.0.0  - run service

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users",
    }
]


app = FastAPI(
    title="OTUS Microservice Architecture",
    description="4th Homework. Users API CRUD",
    summary="",
    version="0.0.2",
   
    contact={
        "name": "Artem Voropay",
        "email": "art_vor@mail.ru"},

    openapi_tags=tags_metadata
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(users.router)
app.include_router(health.router)
