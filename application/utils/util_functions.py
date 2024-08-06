import os
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from api.security import oauth2_scheme
from db.database import get_db
from models.user import User

SECRET_KEY = "6df6e58ffaf7b238d6d54684a14f12c7480015d4d8467dcd784c2b7f143924b0"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update(
            {
                "exp": expires_delta
            }
        )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        # os.getenv("SECRET_KEY"),
        # algorithm=os.getenv("ALGORITHM")
        algorithm=ALGORITHM
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
            # os.getenv("SECRET_KEY"),
            SECRET_KEY,
            # algorithms=[os.getenv("ALGORITHM")]
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user
