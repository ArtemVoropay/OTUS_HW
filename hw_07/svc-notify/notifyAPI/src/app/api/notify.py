from fastapi import APIRouter, Response, status, Request
from typing import Union
from api.models import MessageSchema
from api import db
import datetime
import uuid


router = APIRouter()

# Fake function
async def send(email, text):
    try:
        ## Place your code here
        print(f'SEND MESSAGE TO {email}. TEXT: {text}')
        return True
    except Exception as e:
        return False


@router.post("/notify/", tags=['notify'], description='Send message via E-mail')
async def send_message(payload:MessageSchema, response: Response):
    is_sended = await send(payload.e_mail, payload.text)
    res = await db.log_message(payload, is_sended)

    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST

    return res


@router.get("/notify/{id}", tags=['notify'], description='Get message is_sended status by id')
async def get_message(id:int):
    return  await db.get_message(id)


@router.get("/notify/log/{login}", tags=['notify'],  description='Get messages log by login')
async def get_message_log(login:str):
    return  await db.get_message_log(login)
