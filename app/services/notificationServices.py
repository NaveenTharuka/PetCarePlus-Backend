from app.model.notification import Notification, NotificationCreate, NotificationOut
from app.database_models import Notification as NotificationModel, User, Pet
from app.websocket.manager import manager
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

async def create_notification(notification: NotificationCreate, db: Session):

    db_user = db.query(User).filter(User.id == notification.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_notification = NotificationModel(
        user_id = notification.user_id,
        notification_type = notification.notification_type,
        title = notification.title,
        messege = notification.messege,
        icon = notification.icon,
        read = notification.read,
        created_at = notification.created_at
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    await manager.send_notification(
        str(db_notification.user_id),
        NotificationOut(
            id=db_notification.id,
            user_id=db_notification.user_id,
            notification_type=db_notification.notification_type,
            title=db_notification.title,
            messege=db_notification.messege,
            icon=db_notification.icon,
            read=db_notification.read,
            created_at=db_notification.created_at.isoformat()
        )
    )

    return db_notification

def get_notification(user_id: UUID, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_notification = db.query(NotificationModel).filter(NotificationModel.user_id == user_id).all()
    return db_notification

def create_pet_notification(pet:Pet):

    return NotificationCreate(
        user_id = pet.owner_id,
        notification_type = "PET",
        title = "Pet Created",
        messege = f"{pet.name} has been added to your profile",
        icon = "paw",
        read = False,
        created_at = datetime.utcnow()
    )

