from fastapi import APIRouter, Response, status, Request
from typing import Union
from api.models import OrderSchema
from api import db
import requests
import os

router = APIRouter()


BILLING_URL  = os.getenv("BILLING_URL")
NOTIFY_URL  = os.getenv("NOTIFY_URL")
# BILLING_URL  = "http://arch.homework/billing"
# NOTIFY_URL  = "http://arch.homework/notify"

@router.post("/orders", tags=['order'], description='Create Order')
async def create_order(payload:OrderSchema, response: Response):
  

    # r = requests.get("http://arch.homework/account/a.voropay")
    data = { "login": payload.login,"balance": payload.amount}
    print(data)
    r = requests.post(f"{BILLING_URL}/withdraw", json=data)
    billing_response = r.json()

    print(r.json(), r.status_code)
    if r.status_code == 200:
        message = "Заказ успешно оформлен"
        order_status = 1
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        order_status = 0
        if 'error' in billing_response:
            if billing_response['error'] == 'Not enough money':
                message = f"Недостаточно средств для оформления заказа. Текущий баланс: {r.json()['balance']}.  Сумма заказа: {payload.amount} "
            else:
                message = f"Ошибка в сервисе биллинга: {billing_response}. Обратитесь в Службу поддержки. "


    res = await db.create_order(payload, order_status)
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST

    r = requests.post(f"{NOTIFY_URL}", json={"login":payload.login, 'e_mail': payload.e_mail,  'text' : message})
    
    # print(r.json)


    return res


