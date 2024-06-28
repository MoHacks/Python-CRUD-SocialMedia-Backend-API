from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import SessionLocal, engine, get_db
from .. import dbmodels, schemas, utils
router = APIRouter(tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    
    user = db.query(dbmodels.User).filter(dbmodels.User.email == user_credentials.email).first()

    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    return {"access_token": user.email, "token_type": "bearer"}
    