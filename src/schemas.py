from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint
from datetime import datetime
from typing import Annotated, Optional

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
class PostVote(BaseModel):
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



class Vote(BaseModel):
    post_id: int
    # ge=0, le=1: Specifies that the value of dir must be greater than or equal (ge) to 0 and less than or equal (le) to 1, 
    # restricting it to only 0 or 1.
    dir: int = Field(int, description="Direction of the vote (0 or 1)", ge=0, le=1) # either equal to 0 or 1