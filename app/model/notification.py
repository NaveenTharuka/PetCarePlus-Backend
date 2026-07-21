from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime

class Notification(BaseModel):
    id:UUID
    user_id:UUID
    notification_type:str
    title:str
    messege:str
    icon:str
    read:bool
    created_at:datetime

class NotificationCreate(BaseModel):
    user_id:UUID
    notification_type:str
    title:str
    messege:str
    icon:str
    read:bool
    created_at:datetime

class NotificationOut(Notification):
    model_config = ConfigDict(from_attributes=True)

    