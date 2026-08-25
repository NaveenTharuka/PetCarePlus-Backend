from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.model.appointmanet import AppointmentCreate, AppointmentResponse
from app.model.enum import AppointmentStatus
from app.services import appointmentServices

router = APIRouter()

@router.post("/appointment", response_model=AppointmentResponse)
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return await appointmentServices.create_appointment(appointment, db)


@router.get("/vet/{vet_id}/appointments", response_model=list[AppointmentResponse])
def get_all_vet_appointments(vet_id: UUID, db: Session = Depends(get_db)):
    return appointmentServices.get_all_vet_appointments(vet_id, db)

@router.get("/owner/{owner_id}/appointments", response_model=list[AppointmentResponse])
def get_all_owner_appointments(owner_id: UUID, db: Session = Depends(get_db)):
    return appointmentServices.get_all_owner_appointments(owner_id, db)

@router.put("/appointment/{appointment_id}/status", response_model=AppointmentResponse)
def update_appointment_status(appointment_id: UUID, status: AppointmentStatus, db: Session = Depends(get_db)):
    return appointmentServices.update_appointment_status(appointment_id, status, db)