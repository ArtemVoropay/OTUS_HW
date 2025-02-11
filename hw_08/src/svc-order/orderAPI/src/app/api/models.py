from pydantic import BaseModel, PositiveFloat, PositiveInt
import datetime


class OrderSchema(BaseModel):
    login       : str
    e_mail      : str
    id_product  : int
    quntity     : PositiveInt
    amount      : PositiveFloat
    dtime       : datetime.datetime




