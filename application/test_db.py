# application/test_db.py

from database.database import engine, Base

Base.metadata.create_all(engine)

print("Tables created successfully")
