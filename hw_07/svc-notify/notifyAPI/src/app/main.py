from fastapi import FastAPI, Query, Request
from typing import Optional
from api import notify
from api import health
from api.db import engine, metadata, database
from prometheus_fastapi_instrumentator import Instrumentator

metadata.create_all(engine)



#uvicorn main:app --reload --host 0.0.0.0  - run service

tags_metadata = [
    {
        "name": "Notification service",
        "description": "Notification service",
    }
]


app = FastAPI(
    title="OTUS Microservice Architecture. Notification service",
    description="7th Homework",
    summary="",
    version="0.0.1",
   
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

app.include_router(notify.router)
app.include_router(health.router)

Instrumentator().instrument(app).expose(app)
