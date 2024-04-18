from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2



router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Invalid Credentials")

    verify = utils.verify(user_credentials.password, user.password)
    if not verify:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Invalid Credentials")
    
    access_token = oauth2.create_access_token({"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}