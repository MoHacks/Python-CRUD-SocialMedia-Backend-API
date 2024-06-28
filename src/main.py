from turtle import title
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from random import randrange
import collections
import time
import psycopg2
from . import dbmodels
from .db import SessionLocal, engine, get_db

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

# BaseModel used for schema validation, 
# in this case, its title and content
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #NOTE: Optional field that defaults to True
    
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

# GET used for retreiving data
@app.get("/")
def root():
    return {"nice": "Hello World"}

@app.get("/post")
def get_Post(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(dbmodels.Post).all()
    return {"data:": posts}

# Post pydantic model used for model validation
# the %s is used as a placeholder to pass data to the database, otherwise, the data would be passed in directly as a string,
# making you vulerable to SQL injections 
@app.post("/post", status_code=status.HTTP_201_CREATED)
def make_Post(post: Post, db: Session = Depends(get_db)):

    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
    #                (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # connect.commit()
    # newPost = dbmodels.Post(title=post.title, content=post.content, published=post.published)
    # Converts Post Object to Dictionary
    post = post.model_dump()
    
    # NOTE: unpack the dictionary into the Post Object 
    newPost = dbmodels.Post(**post)
    db.add(newPost)
    db.commit()
    db.refresh(newPost) # NOTE: this will return the newly created post
    return {"data": newPost}


# NOTE: id is initially a STRING, but id: int transformed it into an INT! This is so critical because the 
# next function below expects a string called "latest", if id: int is not used, it will not work because latest will be
# passed into id as a string and it will not be able to find the post because it is a string
@app.get("/post/{id:int}", status_code=status.HTTP_200_OK)
def get_Post_Id(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("SELECT * FROM posts WHERE id = %s", str(id))
    # post = cursor.fetchone()
    
    post = db.query(dbmodels.Post).filter(dbmodels.Post.id == id).first()
    
    return {"data": post}
        
    raise HTTPException(status_code=404, detail=f"post with id of {str(id)} not found with status code 404") 


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
    # deletedPost = cursor.fetchone()

    post = db.query(dbmodels.Post).filter(dbmodels.Post.id == id)

    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return {"message": "post deleted successfully"}
    
    raise HTTPException(status_code=404, detail=f"post with id of {str(id)} not found with status code 404")

@app.put("/post/{id:int}", status_code=status.HTTP_201_CREATED)
def update_Post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
    #                (post.title, post.content, post.published, str(id)))
    # updatedPost = cursor.fetchone()
    
    # if updatedPost:
    #     connect.commit()
    #     return {"message": updatedPost}
    
    postQuery = db.query(dbmodels.Post).filter(dbmodels.Post.id == id)

    postRecord = postQuery.first()
    
    if postRecord:
        
        postQuery.update(post.model_dump(), synchronize_session=False)
        db.commit()
        return {"message": postQuery.first()}
    
    raise HTTPException(status_code=404, detail=f"post with id of {str(id)} not found with status code 404")
    
