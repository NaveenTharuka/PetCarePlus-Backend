from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.model.notification import NotificationCreate, NotificationOut
from app.services import notificationServices
from app.database import get_db
from uuid import UUID
from app.websocket.manager import manager

router = APIRouter()

@router.post("/notifications", response_model=NotificationOut)
async def create_notification(req: NotificationCreate, db: Session = Depends(get_db)):
    return await notificationServices.create_notification(req, db)

@router.get("/notifications/{user_id}", response_model=list[NotificationOut])
async def get_notifications(user_id:UUID, db: Session = Depends(get_db)):
    return await notificationServices.get_notification(user_id, db)


@router.post("/test-notification/{user_id}")
async def test_notification(user_id:str):

    await manager.send_notifications(
        user_id,
        {
            "title":"Test Notification",
            "message":"Realtime is working!",
            "icon":"notifications",
            "type":"test"
        }
    )

    return {
        "message":"sent"
    }