from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.model.notification import NotificationCreate, NotificationOut
from app.services import notificationServices
from app.database import get_db
from uuid import UUID

router = APIRouter()

@router.post("/notification", response_model=NotificationOut)
def create_notification(req: NotificationCreate, db: Session = Depends(get_db)):
    return notificationServices.create_notification(req, db)

@router.get("/notification/{user_id}", response_model=list[NotificationOut])
def get_notifications(user_id:UUID, db: Session = Depends(get_db)):
    return notificationServices.get_notification(user_id, db)