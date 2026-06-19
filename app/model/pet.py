from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Optional, List
from datetime import date
from app.model.report import ReportOut
from app.model.vetVisits import vetVisitOut
from app.model.vaccination import VaccinationOut


class PetBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    colour: Optional[str] = None
    is_registered: bool = False
    gender: Optional[str] = None
    date_of_birth : Optional[date] = None
    weight: Optional[float] = None
    image_url : Optional[str] = None
    profile_pic_id: Optional[UUID] = None

# 🔹 For creating a pet
class PetCreate(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    colour: Optional[str] = None
    is_registered: bool = False
    gender: Optional[str] = None
    date_of_birth : Optional[date] = None
    weight: Optional[float] = None

# 🔹 For updating a pet
class PetEdit(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    weight: Optional[float] = None
    colour: Optional[str] = None
    is_registered: Optional[bool] = None
    gender: Optional[str] = None
    date_of_birth : Optional[date] = None

# 🔹 For returning pet data
class PetOut(PetBase):
    id: UUID
    owner_id: UUID
    vaccinations: List[VaccinationOut] = Field(default_factory=list)
    reports: List[ReportOut] = Field(default_factory=list)
    vet_visits: List[vetVisitOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)