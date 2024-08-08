# application/schema/pizza.py

from typing import Optional
from pydantic import BaseModel


class PizzaBase(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool = True


class PizzaCreate(PizzaBase):
    pass


class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None


class PizzaResponse(PizzaCreate):
    id: int

    class config:
        orm_mode = True


class MessageResponse(BaseModel):
    message: str
