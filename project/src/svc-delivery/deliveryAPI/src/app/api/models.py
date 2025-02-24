from pydantic import BaseModel, PositiveFloat
import datetime


class DeliverySchema(BaseModel):
    id_order    : int
    dtime : datetime.datetime


