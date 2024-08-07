from fastapi import FastAPI
from api.auth import router as user_router
from api.admin import router as admin_router
from api.customer import router as customer_router
from database.database import engine, Base

# create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# including the user router
app.include_router(
    user_router,
    prefix="/users",
    tags=["users"]
)

app.include_router(
    admin_router,
    prefix="/admin",
    tags=["admin"]
)

app.include_router(
    customer_router,
    prefix="/customer",
    tags=["customer"]
)