from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(prefix="/login", tags=["Auth"])


@router.post("/")
def user_login(user_login_info: schemas.UserLogin, db: Session = Depends(get_db)):
    user_info_from_db = (
        db.query(models.User).filter(models.User.email == user_login_info.email).first()
    )
    if not user_info_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
        )
    verified_pass = utils.verify_hashed_password(
        user_login_info.password, user_info_from_db.password
    )
    if not verified_pass:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
        )
    # get a new JWT token
    token = oauth2.create_access_token(payload={"user_id": user_info_from_db.id})
    return {"access_token": token, "token_type": "bearer"}
