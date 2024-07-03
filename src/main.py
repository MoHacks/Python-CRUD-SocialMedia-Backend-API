from email import utils
from turtle import title
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from random import randrange

from . import dbmodels, schemas, utils
from .db import engine
from passlib.context import CryptContext
from .routers import post, user, auth, vote

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


# tell passlib to use bcrypt hashing algorithm 
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# NOTE: No longer needed since we have Alembic, and this is for SQLAlchemy to create the tables
dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()

# To allow for CORS to allow different domains to access the API, must include the following middleware:
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# Include the route for posts from post.py
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# GET used for retreiving data
@app.get("/")
def root():
    return {"success": "API endpoint is up and running"}

