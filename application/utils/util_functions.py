import os
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from database.database import get_db
from models.user import User
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from schema.auth import TokenData, UserResponse

SECRET_KEY = "6df6e58ffaf7b238d6d54684a14f12c7480015d4d8467dcd784c2b7f143924b0"
ALGORITHM = "HS256"
EXPIRE_TIME = 1


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="."
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise credentials_exception

    return user


def role_required(required_role: str, current_user: UserResponse):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if not current_user or current_user.role != required_role:
                raise HTTPException(
                    status_code=401,
                    detail="Operation not permitted"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator