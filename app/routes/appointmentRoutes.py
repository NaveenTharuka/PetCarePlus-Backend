from fastapi import APIRouter
from database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.model.appointmanet import AppointmentCreate, AppointmentResponse
import app.services.appointmentServices

router = APIRouter()

@router.post("/appointment")
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return await appointmentServices.create_appointment(appointment, db)

