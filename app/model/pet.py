from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List

from app.model.vaccination import VaccinationOut


class PetBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    colour: Optional[str] = None
    is_registered: bool
    gender: Optional[str] = None


# 🔹 For creating a pet
class PetCreate(PetBase):
    pass

# 🔹 For updating a pet
class PetEdit(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    colour: Optional[str] = None
    is_registered: Optional[bool] = None
    gender: Optional[str] = None


# 🔹 For returning pet data
class PetOut(PetBase):
    id: UUID
    owner_id: UUID
    vaccinations: List[VaccinationOut] = []

    model_config = ConfigDict(from_attributes=True)