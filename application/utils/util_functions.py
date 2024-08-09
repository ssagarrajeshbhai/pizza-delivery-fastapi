# application/utils/util_functions.py

import os
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from database.database import get_db
from models.user import User
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from schema.auth import TokenData, UserResponse
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_TIME = os.getenv("EXPIRE_TIME")

"""
Function:       create_access_token
Description:    create access token based on the user credentials (if correct).
"""


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="."
)

"""
Function:       get_current_user
Description:    It gets the current logged in user from the token, 
                mainly used for role based access of API endpoints.
"""


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


"""
Function:       role_required (Decorator)
Description:    This decorator is being used with the endpoint to check 
                if the current user accessing the endpoint is authorized to use it or not.
"""


def role_required(allowed_roles: List):
    def decorator(func):
        @wraps(func)
        async def wrapper(
                *args,
                # token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db),
                **kwargs
        ):
            current_user = get_current_user(db)

            if current_user.role not in allowed_roles:
                raise HTTPException(status_code=403, detail="Not authorized")

            return await func(*args, current_user=current_user, db=db, **kwargs)

        return wrapper

    return decorator


"""
Function:       role_validator
Description:    This function takes a list of roles, that are allowed to access the perticular endpoint.
                It also takes current_user and see if any of the listed role matches for current_user.
                If not, raises exception.
                Note: Aim for this function is to be doing role check while role_required decorator is out of service
"""


def role_validator(allowed_roles: List, current_user):
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=401,
            detail="Operation not permitted"
        )

    return True
