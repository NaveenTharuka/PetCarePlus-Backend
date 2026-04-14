from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.model.pet import PetOut

class UserBase(BaseModel):
    name : str
    email : str
    password : str
    role : str
    phone : str
    address : str
    
class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id : UUID
    pets : list[PetOut]

    model_config = ConfigDict(from_attributes=True)