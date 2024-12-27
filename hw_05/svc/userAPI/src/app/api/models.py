from pydantic import BaseModel


class UserSchema(BaseModel):
    login: str
    first_name: str
    middle_name: str
    last_name: str
    age:int
    phone:str
    email:str