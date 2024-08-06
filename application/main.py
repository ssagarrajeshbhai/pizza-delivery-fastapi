from fastapi import FastAPI
from api.users import router as user_router
from db.database import engine, Base

# create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# including the user router
app.include_router(
    user_router,
    prefix="/users",
    tags=["users"]
)