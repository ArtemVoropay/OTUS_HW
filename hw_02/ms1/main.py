
import logging
from fastapi import FastAPI, Query, Request
from typing import Optional

#uvicorn main:app --reload --host 0.0.0.0  - run service

tags_metadata = [
    {
        "name": "root",
        "description": "root route",
    },
    {
        "name": "health",
        "description": "Checks the viability of the service",
      
        },
]


app = FastAPI(
    title="OTUS Microservice Architecture",
    description="2nd Homework",
    summary="",
    version="0.0.1",
   
    contact={
        "name": "Artem Voropay",
        "email": "art_vor@mail.ru"},
  
    openapi_tags=tags_metadata
)

@app.get("/", tags=["root"])
async def root():            
   return {"data": "Test microservice for OTUS :)"}
 
@app.get("/health/", tags = ["health"])
async def health(request: Request):
   return {'status': "OK"}
