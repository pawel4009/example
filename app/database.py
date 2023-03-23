from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# do i have to change this?

# engine is responsible for connecting sqlalchemy to postgres database

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()

# get a session to our database, when request is done, close database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# this could be deleted as we are using sqlalchemy right now!!!!!!!!!!
# while True:
#     try:
#         conn = psycopg2.connect(host= [...], cursor_factory=RealDictCursor
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Conecting to database failed")
#         print("Error: ", error)
#         time.sleep(1)
