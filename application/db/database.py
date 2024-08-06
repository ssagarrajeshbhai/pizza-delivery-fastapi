# database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./pizza_delivery.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    }
)

sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# Dependency to get database session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
