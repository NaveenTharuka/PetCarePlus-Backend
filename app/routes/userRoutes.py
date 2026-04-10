from uuid import UUID
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.user import UserOut
from app.database_models import User


router = APIRouter()

@router.get("/users", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
    
@router.get("/users/{id}",response_model=UserOut)
def get_user_by_id(id : UUID , db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user