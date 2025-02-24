from pydantic import BaseModel, PositiveInt


class StockSchema(BaseModel):
    description    : str
    quantity  : PositiveInt


class StockMoveSchema(BaseModel):
    id: int
    quantity  : PositiveInt
    id_order : PositiveInt

 

