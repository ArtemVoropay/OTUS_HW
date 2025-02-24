from fastapi import APIRouter, Response, status, Request
from typing import Union
from api.models import  DeliverySchema
from api import db

router = APIRouter()



@router.get("/delivery", tags=['delivery'], description='Get Delivery Pool')
async def get_delivery_pool(response: Response):
    res = await db.get_delivery_pool()
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res


@router.post("/delivery", tags=['delivery'], description='Reserve Delivery Slot')
async def reserve_delivery(payload: DeliverySchema):
    res = await db.reserve_delivery(payload)
    return res



   