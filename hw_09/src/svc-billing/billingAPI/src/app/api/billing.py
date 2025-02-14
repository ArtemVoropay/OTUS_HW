from fastapi import APIRouter, Response, status, Request
from typing import Union
from api.models import  RefillSchema
from api import db

router = APIRouter()


@router.post("/billing/register", tags=['billing'], description='Create Account')
async def create_account(login:str, response: Response):
    
    res = await db.create_account(login)
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res


@router.get("/billing/account/{login}", tags=['billing'], description='Get Account Info')
async def get_account(login:str, response: Response):
    res = await db.get_account(login)
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res


@router.post("/billing/refill", tags=['billing'], description='Refill Account balace')
async def refill(payload: RefillSchema):
    res = await db.refill(payload)
    # if res and type(res) == dict and 'error' in res.keys():
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    return res


@router.post("/billing/withdraw", tags=['billing'], description='Withdraw money')
async def withdraw(payload: RefillSchema):    
    res = await db.withdraw(payload)
    # if res and type(res) == dict and 'error' in res.keys():
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    return res
   