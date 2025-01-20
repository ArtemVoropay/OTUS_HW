from fastapi import APIRouter, Response, status, Request
from typing import Union
from api.models import UserSchema, AuthData
from api import db
import jwt
import datetime
import uuid

SECRET_KEY = "OTUS"  #TODO for prod move to env

SESSIONS = {} # TODO  for prod use Redis for sessions

router = APIRouter()

def create_session(user_data):
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = user_data
    return session_id


def make_token(login):
    token = jwt.encode(
        {'login': login,  'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)},
        SECRET_KEY)
    return token


@router.post("/register", tags=['auth'], description='Register new user')
async def register_user(payload:UserSchema, response: Response):
    res = await db.register(payload)
    print(res)
    if res and type(res) == dict and 'error' in res.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST

    return res
    
    
@router.post("/login", tags=['auth'], status_code=200,  description='Login user')
async def login(payload:AuthData, response: Response):
    res =  await db.login(payload)
    if not res: 
        response.status_code = status.HTTP_404_NOT_FOUND
        res = 'User not found'
    elif res == 'password incorrect':
        response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        token = make_token(payload.login)

        response.headers.append('X-User-Id', str(res.id))
        response.headers.append('X-User-Login', res.login)
        response.headers.append('X-User-Firstname', res.first_name)
        response.headers.append('X-User-Lastname', res.last_name)
        response.headers.append('X-User-Email', res.email)
        response.headers.append('X-access-Token', token)
        response.set_cookie(key="access_token", value=token, httponly=True)
        response.set_cookie(key="id_session", value=create_session(res), httponly=True)
    return  res


@router.get("/auth", tags=['auth'],)
async def auth(request: Request, response: Response):
    if 'id_session' in request.cookies.keys(): 
        if  request.cookies['id_session'] in SESSIONS.keys(): 
            res = SESSIONS[request.cookies['id_session']]
            response.headers.append('X-User-Id', str(res.id))
            response.headers.append('X-User-Login', res.login)
            response.headers.append('X-User-Firstname', res.first_name)
            response.headers.append('X-User-Lastname', res.last_name)
            response.headers.append('X-User-Email', res.email)
            response.status_code = status.HTTP_200_OK
            return {'status': 'ok'}
    
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return 'Not Authentificated'
    


@router.get("/logoff", tags=['auth'], description='Logoff user')
def logoff(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="id_session")
    return {'status':'logged off'}


