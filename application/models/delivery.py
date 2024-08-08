# application/models/delivery.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class DeliveryComment(Base):
    __tablename__ = "delivery_comments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    current_user_id = Column(Integer, ForeignKey("users.id"),
                             nullable=False)  # Assuming you have a delivery_persons table
    comment = Column(String, nullable=False)

    orders = relationship("Order", back_populates="delivery_comments")  # Relationship to the Order model
    current_user = relationship("User")  # Assuming you have a DeliveryPerson model
