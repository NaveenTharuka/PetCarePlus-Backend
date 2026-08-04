from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime, date, time

class AppointmentCreate(BaseModel):
    pet_id: UUID
    vet_id: UUID
    appointment_date: date
    appointment_time: time
    reason: str


class AppointmentUpdateStatus(BaseModel):
    status: str


class AppointmentResponse(BaseModel):
    id: UUID
    pet_id: UUID
    owner_id: UUID
    vet_id: UUID
    appointment_date: date
    appointment_time: time
    reason: str
    status: str

    class Config:
        from_attributes = True
