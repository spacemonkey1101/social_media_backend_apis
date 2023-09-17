from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["User"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    # update user password with the hashed password
    new_user.password = utils.hash(new_user.password)
    new_user = models.User(**new_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_info = db.query(models.User).filter(models.User.id == user_id).first()
    if user_info:
        return user_info
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No users found with id : {user_id}",
    )
