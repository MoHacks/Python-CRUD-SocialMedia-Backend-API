from fastapi import APIRouter, FastAPI, Body, Response, status, HTTPException, Depends
from .. import dbmodels, schemas # oath2 has import beyong top-level package
from sqlalchemy.orm import Session
from ..db import SessionLocal, engine, get_db
from typing import Optional, List
from .. import oauth2

# Router is used for grouping related routes
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",  status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post = db.query(dbmodels.Post).filter(dbmodels.Post.id == vote.post_id).first()
    
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(dbmodels.Vote).filter(dbmodels.Vote.post_id == vote.post_id, dbmodels.Vote.user_id == current_user.id)
    
    if vote.dir == 1:
        
        found_vote = vote_query.first()
        
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = dbmodels.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}

    else:
        vote_query = db.query(dbmodels.Vote).filter(dbmodels.Vote.post_id == vote.post_id, dbmodels.Vote.user_id == current_user.id)
        found_vote = vote_query.first()
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}