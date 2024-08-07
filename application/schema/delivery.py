from pydantic import BaseModel
from models.order import OrderStatus
from datetime import datetime

class DeliveryStatusUpdate(BaseModel):
    status: OrderStatus

class DeliveryCommentBase(BaseModel):
    order_id: int
    delivery_person_id: int
    comment: str

class DeliveryCommentCreate(DeliveryCommentBase):
    pass

class DeliveryComment(DeliveryCommentBase):
    id: int
    created_at: datetime

    class config:
        orm_mode=True