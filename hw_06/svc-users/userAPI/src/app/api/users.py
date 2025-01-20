from fastapi import APIRouter, Request
from typing import Union
from api.models import UserSchema
from api import db
import json


router = APIRouter()

@router.post("/users/", tags=['users'], description='Create new user')
async def create_user(payload:UserSchema):
    return await db.insert(payload)
    
    
@router.get("/users/", tags=['users'],)
async def get_user(request: Request):
    try:
        id = int(request.headers.get('x-user-id'))
    except Exception as e:
        return 'Header x-user-id is not allowed'
    return  await db.select_by_id(id)


@router.get("/users", tags=['users'],)
async def get_all_users():
    return  await db.select_all()


@router.put("/users/", tags=['users'], description='Update user by id')
async def update_user(payload:UserSchema, request:Request):
    try:
        id = int(request.headers.get('x-user-id'))
    except Exception as e:
        return 'Header x-user-id is not allowed'
    return await db.update(id, payload)


@router.delete("/users/", tags=['users'], description='Delete user by id')
async def delete_user(id:int):
   return  await db.delete(id)