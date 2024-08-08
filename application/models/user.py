# models/user.py
from sqlalchemy import Column, Integer, String, Enum, Boolean, CheckConstraint
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    username = Column(
        String,
        unique=True,
        index=True,
    )
    email = Column(
        String,
        unique=True,
        index=True,
    )
    hashed_password = Column(
        String,
    )
    role = Column(
        String,
        CheckConstraint("role IN ('customer', 'delivery_partner', 'admin')"),
        index=True,
    )
    is_active = Column(
        Boolean,
        default=True,
    )
    orders = relationship("Order", back_populates="users")
    cart_items = relationship("CartItem", back_populates="users")
