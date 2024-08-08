# FastAPI Pizza Ordering System

This is a FastAPI application for a pizza ordering system. It includes endpoints for customers, delivery persons, and administrators to manage orders, pizzas, and deliveries effectively.

## Table of Contents

- [Customer Endpoints](#customer-endpoints)
  - [Create Order](#create-order)
  - [Get Orders](#get-orders)
  - [Add to Cart](#add-to-cart)
  - [Update Cart](#update-cart)
  - [View Cart](#view-cart)
- [Delivery Person Endpoints](#delivery-person-endpoints)
  - [Update Delivery Status](#update-delivery-status)
  - [Add Delivery Comment](#add-delivery-comment)
- [Admin Endpoints](#admin-endpoints)
  - [Add Pizza](#add-pizza)
  - [Update Pizza](#update-pizza)
  - [Delete Pizza](#delete-pizza)
  - [Update Order Status](#update-order-status)
- [Running the Application](#running-the-application)
- [Authentication and Authorization](#authentication-and-authorization)
- [Database Configuration](#database-configuration)
- [Conclusion](#conclusion)

## Customer Endpoints

### Create Order
- **Endpoint**: `POST /customer/orders`
- **Request Body**:
  ```json
  {
      "user_id": 1,
      "items":[
          {
              "pizza_id": 2,
              "quantity": 1
          },
                  {
              "pizza_id": 6,
              "quantity": 3
          }
      ]
  }
  ```
- **Response**:
  ```json
  {
      "user_id": 1,
      "total_amount": 200.0,
      "created_at": "2024-08-08T05:57:55.256905",
      "updated_at": "2024-08-08T05:57:55.256905",
      "status": "placed",
      "items": [
          {
              "order_id": 13,
              "pizza_id": 2,
              "unit_price": 50.0,
              "id": 22,
              "quantity": 1
          },
          {
              "order_id": 13,
              "pizza_id": 6,
              "unit_price": 50.0,
              "id": 23,
              "quantity": 3
          }
      ]
  }
  ```

### Get Orders
- **Endpoint**: `GET /customer/orders`
- **Response**:
  ```json
  [
    {
        "id": 11,
        "total_amount": 50.0,
        "created_at": "2024-08-08T05:55:28.760200",
        "user_id": 1,
        "status": "placed",
        "updated_at": "2024-08-08T05:55:28.760200"
    },
    {
        "id": 12,
        "total_amount": 200.0,
        "created_at": "2024-08-08T05:57:30.785897",
        "user_id": 1,
        "status": "placed",
        "updated_at": "2024-08-08T05:57:30.785897"
    },
    {
        "id": 13,
        "total_amount": 200.0,
        "created_at": "2024-08-08T05:57:55.256905",
        "user_id": 1,
        "status": "placed",
        "updated_at": "2024-08-08T05:57:55.256905"
    }
  ]
  ```

### Add to Cart
- **Endpoint**: `POST /customer/cart`
- **Request Body**:
  ```json
  {
      "pizza_id": 1,
      "quantity": 2
  }
  ```
- **Response**:
  ```json
  {
      "pizza_id": 1,
      "quantity": 2,
      "id": 1,
      "user_id": 1
  }
  ```

### Update Cart
- **Endpoint**: `PUT /customer/cart/{item_id}`
- **Request Body**:
  ```json
  {
      "quantity": 10
  }
  ```
- **Response**:
  ```json
  {
      "pizza_id": 1,
      "quantity": 10,
      "id": 1,
      "user_id": 1
  }
  ```

### View Cart
- **Endpoint**: `GET /customer/cart`
- **Response**:
  ```json
  {
      "items": [
          {
              "pizza_id": 1,
              "quantity": 10,
              "id": 1,
              "user_id": 1
          }
      ],
      "total": 500.0
  }
  ```

## Delivery Person Endpoints

### Update Delivery Status
- **Endpoint**: `PUT /delivery/deliveries/{order_id}/status`
- **Request Body**:
  ```json
  {
      "status": "preparing"
  }
  ```
- **Response**:
  ```json
  [
      "Order status for order 7 updated from preparing to out_for_delivery"
  ]
  ```
  
  If api call made with the same status again, then it will show the current status
  ```json
  [
    "The current status is out_for_delivery"
  ]
  ```

### Add Delivery Comment
- **Endpoint**: `POST /delivery/deliveries/{order_id}/comments`
- **Request Body**:
  ```json
  {
      "order_id": 1,
      "delivery_person_id": 1,
      "comment": "waiting at your doorstep"
  }
  ```
- **Response**:
  ```json
  {
      "current_user_id": 1,
      "comment": "waiting at your doorstep",
      "id": 5,
      "order_id": 7
  }
  ```

## Admin Endpoints

### Add Pizza
- **Endpoint**: `POST /admin/pizzas`
- **Request Body**:
  ```json
  {
      "name": "dummy pizza",
      "description": "This is for testing purpose only",
      "price": 39,
      "is_available": true
  }
  ```
- **Response**:
  ```json
  {
      "name": "dummy pizza",
      "description": "This is for testing purpose only",
      "price": 39.0,
      "is_available": true,
      "id": 11
  }
  ```

### Update Pizza
- **Endpoint**: `PUT /admin/pizzas/{pizza_id}`
- **Request Body**:
  ```json
  {
      "name": "dummy pizza",
      "description": "Classic cheese pizza for showcase",
      "price": 51
  }
  ```
- **Response**:
  ```json
  {
      "name": "dummy pizza",
      "description": "Classic cheese pizza for showcase",
      "price": 51.0,
      "is_available": true,
      "id": 11
  }
  ```

### Delete Pizza
- **Endpoint**: `DELETE /admin/pizzas/{pizza_id}`
- **Response**:
  ```json
  {
      "message": "Pizza deleted successfully."
  }
  ```

### Update Order Status
- **Endpoint**: `PUT /admin/orders/{order_id}/status`
- **Request Body**:
  ```json
  {
      "status": "delivered"
  }
  ```
- **Response**:
  ```json
  {
      "id": 10,
      "total_amount": 50.0,
      "created_at": "2024-08-08T05:55:09.238627",
      "user_id": 1,
      "status": "delivered",
      "updated_at": "2024-08-08T06:24:31.876080"
  }
  ```

## Running the Application

1. **Install Dependencies**: Run the following command to install required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the FastAPI Server**: Use the following command to start the application:
   ```bash
   cd .\application\
   uvicorn main:app --reload --log-level debug --host 127.0.0.1 --port 8080
   ```
4. **Access the Application**: The application will be available at `http://localhost:8080`.

## Authentication and Authorization

The application uses JWT tokens for authentication. Ensure that you have the necessary configuration and middleware set up.

Roles are used for authorization. Ensure that the appropriate roles are assigned to users and that the `role_required` decorator is used in the endpoints.

## Database Configuration

The application uses SQLAlchemy for database integration. Ensure that you have the correct database connection details configured in your `database.py` file.

## Conclusion

This FastAPI application provides a comprehensive pizza ordering system with endpoints for customers, delivery persons, and administrators. We can always customize and extend the functionality as needed for your specific requirements.
