from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.util_functions import get_current_user, role_required
from schema.auth import TokenData, UserResponse
from schema.pizza import MessageResponse, PizzaCreate, PizzaResponse, PizzaUpdate
from schema.order import Order, OrderUpdate
from database.database import get_db
from models.pizza import Pizza
from models.order import Order as ModelOrder

router = APIRouter()

@router.post("/pizzas", response_model=PizzaResponse)
# @role_required(required_role="admin", current_user=get_current_user)
def create_pizza(
    pizza: PizzaCreate, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
    ):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=401,
            detail="Operation not permitted"
        )
    
    current_pizza = Pizza(
        name=pizza.name,
        description=pizza. description,
        price=pizza.price,
    )

    try:
        db.add(current_pizza)
        db.commit()
        db.refresh(current_pizza)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server Error:" + str(e)
        )

    return current_pizza

@router.put("/pizzas/{pizza_id}", response_model=PizzaResponse)
# @role_required("admin")
def update_pizza(
    pizza_id: int, 
    pizza: PizzaUpdate, 
    db:Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
    ):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=401,
            detail="Operation not permitted"
        )

    pizza_to_update = db.query(Pizza).filter(Pizza.id == pizza_id).first()

    if not pizza_to_update:
        raise HTTPException(status_code=404, detail="Pizza not found")
    
    for key, value in pizza.dict(exclude_unset=True).items():
        setattr(pizza_to_update, key, value)

    db.commit()
    db.refresh(pizza_to_update)

    return pizza_to_update

@router.delete("/pizzas/{pizza_id}", response_model=MessageResponse)
# @role_required("admin", current_user=get_current_user)
def delete_pizza(
    pizza_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401,
            detail="Operation not permitted"
        )
    pizza_to_delete = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza_to_delete:
        raise HTTPException(status_code=404, detail="Pizza not found")
    
    db.delete(pizza_to_delete)
    try:
        db.commit()
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: " + str(e)
        )

    return MessageResponse(message= "Pizza deleted successfully.")

@router.put("/orders/{order_id}/status", response_model=Order)
def update_order_status(
    order_id: int, 
    order_update: OrderUpdate, 
    db: Session = Depends(get_db)
    ):

    # Find the order to update
    order = db.query(ModelOrder).filter(ModelOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update the order status
    order.status = order_update.status
    db.commit()
    db.refresh(order)
    return order