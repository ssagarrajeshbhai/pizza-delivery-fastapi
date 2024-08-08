# application/database/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# databse URL for sqlite database file
DATABASE_URL = os.getenv("DATABASE_URL")

# database engine, using database url
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    }
)

# generate a session
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
