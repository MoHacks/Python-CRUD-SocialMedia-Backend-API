from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from .. import dbmodels, schemas, utils
from sqlalchemy.orm import Session
from ..db import SessionLocal, engine, get_db


router = APIRouter(
    prefix="/user",
    tags=['User']
)
# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def make_User(user: schemas.UserCreate, db: Session = Depends(get_db)):

#     # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
#     #                (post.title, post.content, post.published))
#     # newPost = cursor.fetchone()
#     # connect.commit()
#     # newPost = dbmodels.Post(title=post.title, content=post.content, published=post.published)
#     # Converts Post Object to Dictionary
#     hashedPass = utils.hash(user.password)
#     user.password = hashedPass
    
#     # NOTE: unpack the dictionary into the Post Object 
#     newUser = dbmodels.User(**user.model_dump())
#     db.add(newUser)
#     db.commit()
#     db.refresh(newUser) # NOTE: this will return the newly created post
#     return newUser

# @router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
# def get_User(id: int, db: Session = Depends(get_db)):

#     user = db.query(dbmodels.User).filter(dbmodels.User.id == id).first()

#     if user:
#         return user
    
#     raise HTTPException(status_code=404, detail=f"post with id of {str(id)} not found with status code 404")
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = dbmodels.User(**user.model_dump())   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(dbmodels.User).filter(dbmodels.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user