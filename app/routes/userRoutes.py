from app.services import userServices
from uuid import UUID
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.model.user import UserOut , UserCreate
from app.database_models import User
from app.services.auth import get_current_user
import app.services.userServices

UserServices = app.services.userServices
router = APIRouter()

@router.get("/users", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    db_users = UserServices.get_all_users(db)
    return db_users

@router.get("/user/{user_id}",response_model=UserOut)
def get_user_by_id(user_id : UUID , db : Session = Depends(get_db)):
    db_user = UserServices.get_user_by_id(user_id,db)
    return db_user

@router.post("/user/add", response_model=UserOut)
def create_user(user : UserCreate , db : Session = Depends(get_db)):
    new_user = UserServices.create_user(user,db)
    return new_user

# @router.get("/user/me")
# def get_me(user = Depends(get_current_user)):
#     return user

@router.get("/google_user")
def google_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    user = userServices.google_user(db , authorization)
    return user