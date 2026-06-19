from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr

from app.model.pet import PetOut


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    image_url: Optional[str] = None
    profile_pic_id: Optional[UUID] = None


# 🔹 Create user (password required)
class UserCreate(UserBase):
    password: str


# 🔹 Update user (everything optional)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


# 🔹 Output (NO password here)
class UserOut(UserBase):
    id: UUID
    pets: List[PetOut] = []

    model_config = ConfigDict(from_attributes=True)