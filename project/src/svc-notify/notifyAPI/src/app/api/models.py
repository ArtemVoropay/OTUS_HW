from pydantic import BaseModel


class MessageSchema(BaseModel):
    login   : str
    e_mail  : str
    text    : str


