# schema/schema_user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: str = Field(
        description="User role: customer, delivery_partner, or admin"
    )
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str
