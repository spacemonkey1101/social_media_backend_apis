from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(prefix="/login", tags=["Auth"])


# add OAuth2PasswordRequestForm as a dependency
@router.post("/")
def user_login(
    user_login_info: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # user_login_info with OAuth2PasswordRequestForm
    # has username and password
    user_info_from_db = (
        db.query(models.User)
        .filter(models.User.email == user_login_info.username)
        .first()
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
