from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from .. import dbmodels, schemas, utils
from sqlalchemy.orm import Session
from ..db import SessionLocal, engine, get_db


router = APIRouter(
    prefix="/user",
    tags=['User']
)

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