from pydantic import BaseModel, PositiveFloat


class RefillSchema(BaseModel):
    login    : str
    balance  : PositiveFloat


