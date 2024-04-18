from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    hash_password = utils.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=List[schemas.User])
def get_user(db : Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@router.get('/{id}', response_model=schemas.User)
def get_user(id : int, db : Session = Depends(get_db)):
    user =  db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'User with an id {id} wasn\'t found')
    return user


@router.delete('/{id}')
def delete_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'User with an id {id} doean\'t exist')
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.User)
def update_user(id : int, user : schemas.UserCreate, db : Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'User with an id {id} doean\'t exist')
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()