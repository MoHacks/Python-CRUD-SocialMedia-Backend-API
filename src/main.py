from email import utils
from turtle import title
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import collections
import time
import psycopg2
from . import dbmodels, schemas, utils
from .db import SessionLocal, engine, get_db
from passlib.context import CryptContext
from .routers import post, user, auth

# tell passlib to use bcrypt hashing algorithm 
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()

# To allow for CORS to allow different domains to access the API, must include the following middleware:
# app.include_router(api.router)
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


'''
Fast-API has built-in SWAGGER UI: http://localhost:8000/docs
Fast-API has built-in redoc UI: http://localhost:8000/redoc

COMMON STATUS CODES: 
200: OK (when retrieving)
201: CREATED (when creating)
204: NO CONTENT (when deleting)
400: BAD REQUEST (when bad request)
404: NOT FOUND (when not found)
500: INTERNAL SERVER ERROR (when server error)


CRUD OPERATIONS: Create, Read, Update, Delete
HTTP MAIN METHODS: GET, POST, PUT (pass all fields)/Patch(pass subset of fields), DELETE

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

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "pizza", "id": 2}]


# Include the route for posts from post.py
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# GET used for retreiving data
@app.get("/")
def root():
    return {"nice": "Hello World"}

