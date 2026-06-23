from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Optional, List
from datetime import date

class vetVisitBase(BaseModel):
    id: UUID
    pet_id: UUID
    vet_name: str
    visit_date: date
    reason: str
    note:str

class vetVisitCreate(BaseModel):
    pet_id: UUID
    vet_name: str
    visit_date: date
    reason: str
    note:Optional[str] = None

class vetVisitUpdate(BaseModel):
    visit_id:UUID
    vet_name: Optional[str] = None
    visit_date: Optional[date] = None
    reason: Optional[str] = None
    note:Optional[str] = None

class vetVisitOut(vetVisitBase):
    model_config = ConfigDict(from_attributes=True)
