from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class PetBase(BaseModel):
    name: str
    type: str
    breed: str
    color: str
    isRegistered : bool

class PetCreate(PetBase):
    owner_id: Optional[UUID]

class PetOut(PetBase):
    id : UUID
    owner_id: Optional[UUID]
    model_config = ConfigDict(from_attributes=True)