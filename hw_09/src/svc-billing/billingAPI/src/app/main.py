from fastapi import FastAPI, Query, Request
from typing import Optional
from api import billing
from api import health
from api.db import engine, metadata, database
from prometheus_fastapi_instrumentator import Instrumentator
from api.rpc import consume
import asyncio

metadata.create_all(engine)

#uvicorn main:app --reload --host 0.0.0.0  - run service

tags_metadata = [
    {
        "name": "Billing service",
        "description": "Billing service",
    }
]


app = FastAPI(
    title="OTUS Microservice Architecture. Billing service",
    description="8th Homework",
    summary="",
    version="0.0.3",
   
    contact={
        "name": "Artem Voropay",
        "email": "art_vor@mail.ru"},

    openapi_tags=tags_metadata
)

@app.on_event("startup")
async def startup():
    await database.connect()
    asyncio.ensure_future(consume())

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(billing.router)
app.include_router(health.router)

Instrumentator().instrument(app).expose(app)
