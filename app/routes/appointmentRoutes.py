from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.model.appointmanet import AppointmentCreate, AppointmentResponse
from app.services import appointmentServices

router = APIRouter()

@router.post("/appointment")
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return await appointmentServices.create_appointment(appointment, db)


@router.get("/vet/{vet_id}/appointments", response_model=list[AppointmentResponse])
def get_all_vet_appointments(vet_id: UUID, db: Session = Depends(get_db)):
    return appointmentServices.get_all_vet_appointments(vet_id, db)

@router.get("/owner/{owner_id}/appointments", response_model=list[AppointmentResponse])
def get_all_owner_appointments(owner_id: UUID, db: Session = Depends(get_db)):
    return appointmentServices.get_all_owner_appointments(owner_id, db)