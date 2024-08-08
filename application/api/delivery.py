# application/api/delivery.py

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

"""
Endpoint:       PUT /delivery/deliveries/{order_id}/status
Function:       update_delivery_status
Description:    Validate the order form request json, 
                if present, it updates the status from old status to status given by delivery_person.
                Also if the current_status is same as new_status, it shows current_status.              
"""


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

    return {f"Order status for order {order_id} updated from {prev_status} to {status_update.status}"}


"""
Endpoint:       POST /delivery/deliveries/{order_id}/comments
Function:       add_delivery_comment
Description:    The delivery person can add the comment to the order using this function.               
"""


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
