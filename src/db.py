from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from sqlalchemy.exc import SQLAlchemyError
from .config import settings


# Provided on fastAPI documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
                        
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# if you wish to connect to database using raw SQL
'''
while True:
    try: 
        connect = psycopg2.connect(
            host="localhost",
            database="backendDB",
            user="postgres",
            password="postgres"
        )
        cursor = connect.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database connection failed: ", error)
        time.sleep(2)
'''

