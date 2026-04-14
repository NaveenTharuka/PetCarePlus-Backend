from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date
from typing import Optional

class PetBase(BaseModel):
    owner_id: Optional[UUID]
    name: str
    species: str
    breed: str
    colour: str
    isRegistered : bool
    gender : str
    nextVaccination : date
    

class PetCreate(PetBase):
    pass

class PetOut(PetBase):
    id : UUID
    model_config = ConfigDict(from_attributes=True)

class PetEdit(BaseModel):
    name: str
    p_type: str
    breed: str
    colour: str
    isRegistered : bool
