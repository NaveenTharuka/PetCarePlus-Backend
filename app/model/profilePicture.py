from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class profilePictureBase(BaseModel):
    user_id: Optional[UUID] = None
    pet_id:Optional[UUID] = None
    name:str
    id: UUID
    file_path:str

class profilePictureCreate(profilePictureBase):
    pass

class profilePictureUpdate(profilePictureBase):
    model_config = ConfigDict(from_attributes=True)