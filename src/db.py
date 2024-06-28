from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from sqlalchemy.exc import SQLAlchemyError


# Provided on fastAPI documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/backendDB"

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

