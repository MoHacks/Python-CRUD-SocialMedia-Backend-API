from fastapi import APIRouter, FastAPI, Body, Response, status, HTTPException, Depends
from .. import dbmodels, schemas, utils
from sqlalchemy.orm import Session
from ..db import SessionLocal, engine, get_db
from typing import Optional, List

# Router is used for grouping related routes
router = APIRouter(
    prefix="/post",
    tags=['Post']
)

@router.get("/", response_model=List[schemas.Post])
def get_Post(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(dbmodels.Post).all()
    return posts

# Post pydantic model used for model validation
# the %s is used as a placeholder to pass data to the database, otherwise, the data would be passed in directly as a string,
# making you vulerable to SQL injections 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def make_Post(post: schemas.PostCreate, db: Session = Depends(get_db)):

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
    return newPost


# NOTE: id is initially a STRING, but id: int transformed it into an INT! This is so critical because the 
# next function below expects a string called "latest", if id: int is not used, it will not work because latest will be
# passed into id as a string and it will not be able to find the post because it is a string
@router.get("/{id:int}", status_code=status.HTTP_200_OK)
def get_Post_Id(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("SELECT * FROM posts WHERE id = %s", str(id))
    # post = cursor.fetchone()
    
    post = db.query(dbmodels.Post).filter(dbmodels.Post.id == id).first()
    
    return post
         

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
    # deletedPost = cursor.fetchone()

    post = db.query(dbmodels.Post).filter(dbmodels.Post.id == id)

    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return {"message": "post deleted successfully"}
    
    raise HTTPException(status_code=404, detail=f"post with id of {str(id)} not found with status code 404")

@router.put("/{id:int}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_Post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
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
        return postQuery.first()
    
    raise HTTPException(status_code=404, detail=f"post with id of {str(id)} not found with status code 404")