from app.model.notification import Notification, NotificationCreate, NotificationOut
from app.database_models import Notification as NotificationModel, User
from sqlalchemy.orm import Session
from uuid import UUID

def create_notification(notification: NotificationCreate, db: Session):

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

    return db_notification

def get_notification(user_id: UUID, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_notification = db.query(NotificationModel).filter(NotificationModel.user_id == user_id).all()
    return db_notification