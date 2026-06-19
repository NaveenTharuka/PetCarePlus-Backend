from sqlalchemy.orm import Session
from fastapi import HTTPException, Header
from uuid import UUID

from app.database_models import User
from app.services.reportUploadServices import delete_profile_picture
from app.model.user import UserCreate, UserUpdate
from app.supabase import supabase


# 🔹 Create User
def create_user(user: UserCreate, db: Session):
    exists_user = db.query(User).filter(User.email == user.email).first()

    if exists_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role,
        phone=user.phone,
        address=user.address,
        image_url=user.image_url
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# 🔹 Get All Users
def get_all_users(db: Session):
    db_users = db.query(User).all()

    return db_users

# 🔹 Get User by ID
def get_user_by_id(user_id: UUID, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# 🔹 Delete User
async def delete_user_by_id(user_id: UUID, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.profile_pic_id:
        await delete_profile_pic(db, db_user.profile_pic_id)

    db.delete(db_user)
    db.commit()

    return {"message": "User deleted successfully"}


# 🔹 Update User (PATCH style)
def update_user(user_id: UUID, user: UserUpdate, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

def google_user(db:Session, authorization:str=Header(...) ):

    token = authorization.replace("Bearer", "").strip()

    data =  supabase.auth.get_user(token)

    if not data or not data.user:
        raise HTTPException(
            status_code=404,
            detail="Invalid token"
        )

    new_user = data.user
    db_user = db.query(User).filter(new_user.email == User.email).first()

    if db_user:
        return db_user

    db_new_user = User(
        id=new_user.id,
        name=new_user.user_metadata.get("full_name"),
        email=new_user.email,
        password=None,
        role="user",
        phone=None,
        address=None,
        image_url=new_user.user_metadata.get("picture")
    )

    db.add(db_new_user)
    db.commit()
    db.refresh(db_new_user)

    return db_new_user
    