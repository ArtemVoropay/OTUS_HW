from fastapi import APIRouter, Response, status, Request
from typing import Union
from api.models import  StockSchema, StockMoveSchema
from api import db

router = APIRouter()


@router.post("/stock/register", tags=['stock'], description='Create stock position')
async def create_position(payload: StockSchema, response: Response):
    
    res = await db.create_position(payload)
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res



@router.get("/stock", tags=['stock'], description='Get all positions')
async def get_products(response: Response):
    res = await db.get_all_products()
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res


@router.get("/stock/{id}", tags=['stock'], description='Get position Info')
async def get_product(id:int, response: Response):
    res = await db.get_product(id)
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res


# @router.post("/stock/refill", tags=['stock'], description='Refill position count')
async def refill(payload: StockMoveSchema):
    res = await db.refill(payload)
    return res


# @router.post("/billing/withdraw", tags=['billing'], description='Withdraw money')
async def reserve(payload: StockMoveSchema):    
    res = await db.withdraw(payload)
    # if res and type(res) == dict and 'error' in res.keys():
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    return res
   