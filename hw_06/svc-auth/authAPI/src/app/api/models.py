from pydantic import BaseModel


class UserSchema(BaseModel):
    login: str
    first_name: str
    last_name: str
    email:str
    password:str

class AuthData(BaseModel):
    login: str
    password:str