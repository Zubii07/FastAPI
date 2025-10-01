

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas
from fastapi import HTTPException,status
from ..hashing import Hash

def create(request: schemas.User,db:Session):
    # Check if user with this email already exists
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = models.User(name=request.name,email=request.email,password=Hash.argon2(request.password))
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

def show(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user
