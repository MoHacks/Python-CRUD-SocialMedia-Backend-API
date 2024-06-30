from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

# BaseModel used for schema validation, and as a base class for other schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# 
class PostCreate(PostBase):
    pass

# WE DO NOT INCLUDE PASSWORD IN HERE SINCE WE ARE RETURNING DATA TO THE USER AFTER IT HAS ALREADY INPUT ITS PASSWORD,
# SO NO NEED TO RETURN THE PASSWORD BACK TO THE USER, therefore we dont include password as a field in UserOut
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # NOTE: orm_mode = True allows pydantic to map ORM objects (from databases or other structured data sources) 
    # directly to instances of UserOut so that SQLAlchemy can interface with the database
    class Config:
        orm_mode = True

#
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

# 
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


# Creates user
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# logs in user
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 
class Token(BaseModel):
    access_token: str
    token_type: str

# 
class TokenData(BaseModel):
    id: Optional[int] = None


# class Vote(BaseModel):
#     post_id: int
#     dir: conint(le=1)