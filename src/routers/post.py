from fastapi import APIRouter, FastAPI, Body, Response, status, HTTPException, Depends
from sqlalchemy import func
from .. import dbmodels, schemas # oath2 has import beyong top-level package
from sqlalchemy.orm import Session
from ..db import SessionLocal, engine, get_db
from typing import Optional, List
from .. import oauth2

# Router is used for grouping related routes
router = APIRouter(
    prefix="/post",
    tags=['Post']
)

@router.get("/", response_model=List[schemas.PostVote])
def get_Post(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), 
             limit: int = 8, skip: int = 0, search: Optional[str] = ""):

    # SQLAlchemy automatically makes join default to LEFT INNER JOIN
    posts = db.query(dbmodels.Post, func.count(dbmodels.Vote.post_id).label("votes")).join(dbmodels.Vote, dbmodels.Post.id == dbmodels.Vote.post_id, isouter=True).group_by(dbmodels.Post.id).filter(dbmodels.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

# Post pydantic model used for model validation
# the %s is used as a placeholder to pass data to the database, otherwise, the data would be passed in directly as a string,
# making you vulerable to SQL injections 

# NOTE: get_current_user 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def make_Post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post = post.model_dump()
    
    # NOTE: unpack the dictionary into the Post Object 
    newPost = dbmodels.Post(owner_id=current_user.id, **post) # **post.model_dump() spreads schema out to individual fields

    db.add(newPost)
    db.commit()
    db.refresh(newPost) # NOTE: this will return the newly created post
    return newPost


# NOTE: id is initially a STRING, but id: int transformed it into an INT! This is so critical because the 
# next function below expects a string called "latest", if id: int is not used, it will not work because latest will be
# passed into id as a string and it will not be able to find the post because it is a string
# The response_model is used to define the schema of the response when returned from the function (as defined by 
# the schemas.py file)
@router.get("/{id:int}", status_code=status.HTTP_200_OK, response_model=schemas.PostVote)
def get_Post_Id(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    post = db.query(dbmodels.Post, func.count(dbmodels.Vote.post_id).label("votes")).join(dbmodels.Vote, dbmodels.Post.id == dbmodels.Vote.post_id, isouter=True).group_by(dbmodels.Post.id).filter(dbmodels.Post.id == id).first()
    
    return post
         

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    postQuery = db.query(dbmodels.Post).filter(dbmodels.Post.id == id)

    postRecord = postQuery.first()
    # first check if the owner of the post is the current user, if not, raise an error
    if postRecord.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    

    if postRecord:
        postQuery.delete(synchronize_session=False)
        db.commit()
    
    return Response(status_code=404)

@router.put("/{id:int}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_Post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    postQuery = db.query(dbmodels.Post).filter(dbmodels.Post.id == id)

    postRecord = postQuery.first()
    
    # first check if the owner of the post is the current user, if not, raise an error
    if postRecord.owner_id != current_user.id:
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    if postRecord:
        postQuery.update(post.model_dump(), synchronize_session=False)
        db.commit()
        return postQuery.first()
    
    raise HTTPException(status_code=404, detail=f"post with id of {str(id)} not found with status code 404")

