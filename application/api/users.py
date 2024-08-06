from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db.database import get_db
from models.user import User
from schema.schema_user import UserCreate, UserResponse, UserLogin

from utils.util_functions import create_access_token, get_current_user

router = APIRouter()

# password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# User registration
@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # check if user already exist
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server Error:" + str(e)
        )

    return db_user


# User Login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detaols="Invalid Credentials")

    access_token = create_access_token(
        data={"sub": db_user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Get current User
@router.get("/me", response_model=UserResponse)
def read_users_me(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return current_user


# Update User Detail
@router.put("/me", response_model=UserResponse)
def update_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.email = user.email
    current_user.role = user.role
    current_user.is_active = user.is_active

    db.commit()
    db.refresh(current_user)

    return current_user


# Deactivate User Account
@router.delete("/me")
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()

    return {
        "Message": "User account Deactivated successfully"
    }
