from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/login", tags=["Auth"])

@router.post("/")
def user_login( db: Session = Depends(get_db)):
    pass