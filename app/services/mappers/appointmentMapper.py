from app.model.appointmanet import AppointmentResponse, AppointmentCreate
from app.database_models import Appointment,User,Pet
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID

def to_appointment_response(appointment: Appointment, db:Session):

    owner = db.query(User).filter(User.id == appointment.owner_id).first()
    vet = db.query(User).filter(User.id == appointment.vet_id).first()
    pet = db.query(Pet).filter(Pet.id == appointment.pet_id).first()

    return AppointmentResponse(
        id=appointment.id,
        pet=pet.name,
        owner=owner.name,
        vet_id=appointment.vet_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason,
        status=appointment.status,
        avatar=pet.image_url or ""
    )

def create_appointment(appointment:AppointmentCreate, owner_id:UUID):
    return Appointment(
        pet_id=appointment.pet_id,
        vet_id=appointment.vet_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason,
        status=appointment.status,
        owner_id=owner_id
    )