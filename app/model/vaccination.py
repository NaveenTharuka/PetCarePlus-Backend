from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from uuid import UUID
from datetime import date
from typing import Optional


class VaccinationBase(BaseModel):
    pet_id : UUID = Field(validation_alias=AliasChoices('pet_id', 'petId'))
    vaccineName : str = Field(validation_alias=AliasChoices('vaccineName', 'vaccine_name'))
    vaccineDate : date = Field(validation_alias=AliasChoices('vaccineDate', 'vaccine_date'))
    dueDate : Optional[date] = Field(default=None, validation_alias=AliasChoices('dueDate', 'next_due_date'))
    vetName : Optional[str] = Field(default=None, validation_alias=AliasChoices('vetName', 'vet_name'))
    notes : Optional[str] = None

class VaccinationCreate(VaccinationBase):
    pass

class VaccinationOut(VaccinationBase):
    id : UUID
    model_config = ConfigDict(from_attributes=True)

class VaccinationEdit(BaseModel):
    vaccineName : str 
    vaccineDate : date
    dueDate : Optional[date]
    vetName : Optional[str]
    notes : Optional[str]