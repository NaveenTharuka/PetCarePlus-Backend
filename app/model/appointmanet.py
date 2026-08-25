from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime, date, time
from app.model.enum import AppointmentStatus

class AppointmentCreate(BaseModel):
    pet_id: UUID
    vet_id: UUID
    appointment_date: date
    appointment_time: time
    reason: str
    status: Optional[AppointmentStatus] = AppointmentStatus.PENDING


class AppointmentUpdateStatus(BaseModel):
    status: AppointmentStatus


class AppointmentResponse(BaseModel):
    id: UUID
    pet: str
    owner: str
    vet_id: UUID
    appointment_date: date
    appointment_time: time
    reason: str
    status: AppointmentStatus
    avatar: str

    class Config:
        from_attributes = True
