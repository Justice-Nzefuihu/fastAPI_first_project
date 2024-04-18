from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2, schemas, models


router = APIRouter(
    prefix="/votes",
    tags=["Vote"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote( vote : schemas.Vote, db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id of {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status.HTTP_409_CONFLICT, f"user {current_user.id} has alraedy voted on post {vote.post_id}")
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not vote_found:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"mesage": "successfully deleted vote"}