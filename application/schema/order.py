from pydantic import BaseModel
from datetime import datetime
from models.order import OrderStatus

class OrderItemBase(BaseModel):
    pizza_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    unit_price: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    items: list[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: OrderStatus

class Order(OrderBase):
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: list[OrderItem]

    class Config:
        orm_mode = True
