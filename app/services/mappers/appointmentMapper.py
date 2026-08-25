from app.model.appointmanet import AppointmentResponse, AppointmentCreate
from app.database_models import Appointment, User, Pet
from app.model.enum import AppointmentStatus
from sqlalchemy.orm import Session
from uuid import UUID

def to_appointment_response(appointment: Appointment, db: Session):
    owner = db.query(User).filter(User.id == appointment.owner_id).first()
    vet = db.query(User).filter(User.id == appointment.vet_id).first()
    pet = db.query(Pet).filter(Pet.id == appointment.pet_id).first()

    status_val = appointment.status
    if isinstance(status_val, str):
        status_val = AppointmentStatus(status_val)

    return AppointmentResponse(
        id=appointment.id,
        pet=pet.name if pet else "",
        owner=owner.name if owner else "",
        vet_id=appointment.vet_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason or "",
        status=status_val,
        avatar=pet.image_url if pet and pet.image_url else ""
    )

def create_appointment(appointment: AppointmentCreate, owner_id: UUID):
    return Appointment(
        pet_id=appointment.pet_id,
        vet_id=appointment.vet_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason,
        status=appointment.status or AppointmentStatus.PENDING,
        owner_id=owner_id
    )