from typing import Optional

from pydantic import BaseModel


class PizzaCreate(BaseModel):
    name: str
    description: str
    price: float


class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None


class PizzaResponse(PizzaCreate):
    id: int

    class config:
        orm_mode = True
