from sqlalchemy.orm import Session
from app.model.user import UserCreate, UserUpdate
from app.database_models import User
from fastapi import HTTPException
from uuid import UUID

# Add User
def create_user(user : UserCreate, db : Session):
    exists_user = db.query(User).filter(User.email == UserCreate.email).first()

    if exists_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(
        name = user.name,
        email = user.email,
        password = user.password,
        role = user.role,
        phone = user.phone,
        address = user.address
    )

    db.add(db_user)
    db.commit
    db.refresh(db_user)

    return db_user

# Get user by id
def getUserById(user_id : UUID, db : Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete user by id
def deleteUserById(user_id: UUID, db:Session):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return HTTPException(status_code=200, detail="User deleted successfully")

# Update user
def updateUser(user_id:UUID ,user: UserUpdate, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = User(
        name = user.name,
        email = user.email,
        role = user.role,
        password = user.password,
        phone = user.phone,
        address = user.address
    )

    db.commit()
    db.refresh(db_user)

    return db_user
