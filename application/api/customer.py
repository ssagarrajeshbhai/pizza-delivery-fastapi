# application/api/customer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.cart import CartItem, CartItemCreate, CartItemUpdate, Cart
from schema.pizza import PizzaResponse
from schema.order import OrderCreate, Order, OrderItem
from utils.util_functions import get_current_user
from schema.auth import UserResponse
from database.database import get_db
from models.pizza import Pizza
from models.cart import CartItem as ModelCartItem
from models.order import OrderItem as ModelOrderItem, Order as ModelOrder
from typing import List

router = APIRouter()


@router.get("/pizzas", response_model=list[PizzaResponse])
def get_pizzas(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user),
):
    pizzas = db.query(Pizza).filter(Pizza.is_available == True).all()
    return pizzas


@router.post("/cart", response_model=CartItem)
def add_to_cart(
        cart_item: CartItemCreate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    # Check if pizza exist
    db_pizza = db.query(Pizza).filter(Pizza.id == cart_item.pizza_id).first()
    if not db_pizza:
        raise HTTPException(
            status_code=404,
            detail="Pizza not found"
        )

    # Check if the cart already exist for the user
    user_cart = db.query(ModelCartItem).filter(
        ModelCartItem.user_id == current_user.id,
        ModelCartItem.pizza_id == cart_item.pizza_id
    ).first()

    if user_cart:
        # update the quantity
        user_cart.quantity += cart_item.quantity
        db.commit()
        db.refresh(user_cart)
        return user_cart

    else:
        # create a new cart
        new_item = ModelCartItem(
            user_id=current_user.id,
            pizza_id=cart_item.pizza_id,
            quantity=cart_item.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return new_item


@router.put("/cart/{item_id}", response_model=CartItem)
def update_cart(
        item_id: int,
        cart_item_update: CartItemUpdate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    # Find the cart item to update
    item_to_update = db.query(ModelCartItem).filter(
        ModelCartItem.id == item_id, ModelCartItem.user_id == current_user.id
    ).first()

    if not item_to_update:
        raise HTTPException(
            status_code=404,
            detail="Item not found in cart"
        )

    # Update the quantity
    item_to_update.quantity = cart_item_update.quantity
    db.commit()
    db.refresh(item_to_update)

    return item_to_update


@router.get("/cart", response_model=Cart)
def view_cart(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    # Retrieve the user's cart items
    cart_items = list(db.query(ModelCartItem).filter(ModelCartItem.user_id == current_user.id).all())
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Calculate the total price
    total = sum(item.quantity * item.pizza.price for item in cart_items)
    return {
        "items": cart_items,
        "total": total
    }


@router.delete("/cart/{item_id}")
def delete_cart_item(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    # Find the cart item to delete
    item_to_delete = db.query(ModelCartItem).filter(
        ModelCartItem.id == item_id,
        ModelCartItem.user_id == current_user.id
    ).first()

    if not item_to_delete:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(item_to_delete)
    db.commit()
    return {"Item got deleted"}


@router.post("/orders")
def create_order(
        order_create: OrderCreate,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    # Calculate total amount and validate pizzas
    total_amount = 0
    order_items = []

    for item in order_create.items:
        # Check if the pizza exists
        db_pizza = db.query(Pizza).filter(Pizza.id == item.pizza_id).first()
        if not db_pizza:
            raise HTTPException(
                status_code=404,
                detail=f"Pizza with id {item.pizza_id} not found"
            )

        # Calculate the total amount
        total_amount += db_pizza.price * item.quantity

        # Create order item
        order_item = ModelOrderItem(
            pizza_id=item.pizza_id,
            quantity=item.quantity,
            unit_price=db_pizza.price
        )
        order_items.append(order_item)

    # Create the order
    new_order = ModelOrder(
        user_id=current_user.id,
        total_amount=total_amount,
        order_items=order_items  # This will create the relationship
    )

    # Query the items in the order
    # items_in_order = db.query(ModelOrderItem).filter(
    #     ModelOrderItem.order_id == new_order.id
    # ).all()

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {
        "user_id": current_user.id,
        "total_amount": total_amount,
        "created_at": new_order.created_at,
        "updated_at": new_order.updated_at,
        "status": new_order.status,
        "items": new_order.order_items
    }


# @router.get("/orders", response_model=list[Order])
@router.get("/orders")
def get_orders(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    # Retrieve all orders for the current user
    orders = db.query(ModelOrder).filter(ModelOrder.user_id == current_user.id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    return orders
