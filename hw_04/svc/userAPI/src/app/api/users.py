from fastapi import APIRouter
from typing import Union
from api.models import UserSchema
from api import db
import json


router = APIRouter()

@router.post("/user/", tags=['users'], description='Create new user')
async def create_user(payload:UserSchema):
    return await db.insert(payload)
    
    
@router.get("/users/{id}", tags=['users'],)
async def get_user(id:int = 1):
    return  await db.select_by_id(id)


@router.get("/users", tags=['users'],)
async def get_all_users():
    return  await db.select_all()


@router.put("/user/", tags=['users'], description='Update user by id')
async def update_user(id:int, payload:UserSchema):
    return await db.update(id,payload)


@router.delete("/user/", tags=['users'], description='Delete user by id')
async def delete_user(id:int):
   return  await db.delete(id)