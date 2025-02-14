from fastapi import APIRouter, Response, status, Request
from typing import Union
from api.models import OrderSchema
from api import db
from api.rpc import publish
import json

router = APIRouter()



@router.post("/orders", tags=['order'], description='Create Order')
async def create_order(payload:OrderSchema, response: Response, request: Request):
    if not 'x-request-id' in request.headers:
        return {'error': 'x-request-id is not presented in headers'}
    
    req_id = request.headers['x-request-id']

    order_status = 'Payment Waiting'

    res = await db.create_order(payload, order_status, request_id=req_id)
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
    else:
        print({"id":res.request_id, "login": res.login,"balance": res.amount})
        await publish("withdrawMoney", json.dumps({"order_id":res.id, "login": res.login, "amount": res.amount}))
   
    return res


@router.get("/orders/last", tags=['order'], description='Get last order')
async def get_last_order( response: Response):
 
    res = await db.get_last_order()
 
    return res


async def set_order_status(id, status):
    await db.set_order_status(id,status)


