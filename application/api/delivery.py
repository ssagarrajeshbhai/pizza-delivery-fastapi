from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.util_functions import get_current_user
from schema.auth import UserResponse
from schema.order import Order
from schema.delivery import DeliveryStatusUpdate, DeliveryComment, DeliveryCommentCreate
from models.order import Order as ModelOrder
from models.delivery import DeliveryComment as ModelDeliveryComment
from database.database import get_db



router = APIRouter()

@router.put("/deliveries/{order_id}/status")
def update_delivery_status(
    order_id: int, 
    status_update: DeliveryStatusUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
    ):

    # Find the order to update
    order = db.query(ModelOrder).filter(ModelOrder.id == order_id).first()
    prev_status = order.status

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # return if the current and status to update is same
    if prev_status == status_update.status:
        return {f"The current status is {prev_status}"}

    # Update the delivery status
    order.status = status_update.status
    db.commit()
    db.refresh(order)

    return { f"Order status updated from {prev_status} to {status_update.status}"}

# @router.post("/deliveries/{order_id}/comments", response_model=ModelDeliveryComment)
@router.post("/deliveries/{order_id}/comments")
def add_delivery_comment(
    order_id: int, 
    comment_create: DeliveryCommentCreate, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
    ):

    # Find the order
    order = db.query(ModelOrder).filter(ModelOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Create the delivery comment
    new_comment = ModelDeliveryComment(
        order_id=order.id,
        current_user_id=current_user.id,
        comment=comment_create.comment
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment