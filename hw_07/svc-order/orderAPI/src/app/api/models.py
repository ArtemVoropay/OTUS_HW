from pydantic import BaseModel, PositiveFloat, PositiveInt


class OrderSchema(BaseModel):
    login    : str
    e_mail    : str
    id_cart  : int
    amount   : PositiveFloat




