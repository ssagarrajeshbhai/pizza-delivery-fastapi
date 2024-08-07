from pydantic import BaseModel

class CartItemBase(BaseModel):
    pizza_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItem(CartItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class Cart(BaseModel):
    items: list[CartItem]
    total: float

    class Config:
        orm_mode = True