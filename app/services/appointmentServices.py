from app.model.appointmanet import AppointmentCreate, AppointmentResponse, AppointmentUpdateStatus
from app.database_models import Appointment, User, Pet
from app.services import notificationServices

from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException


async def create_appointment(appointment: AppointmentCreate,owner_id:UUID, db: Session):

    pet = db.query(Pet).filter(Pet.id == appointment.pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    vet = db.query(User).filter(User.id == appointment.vet_id).first()
    if not vet:
        raise HTTPException(status_code=404, detail="Vet not found")
    if not vet.role == "VET":
        raise HTTPException(status_code=404, detail="User is not a vet")

    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    if not owner.id == pet.owner_id:
        raise HTTPException(status_code=404, detail="Owner is not the owner of the pet")
    

    db_appointment = Appointment(
        pet_id=appointment.pet_id,
        vet_id=appointment.vet_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason,
        status=appointment.status,
        owner_id=owner_id
    )
    
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    appointment_notification = notificationServices.create_appointment_notification(db_appointment, db)
    await notificationServices.create_notification(appointment_notification, db)
    
    return db_appointment

def get_all_vet_appointments(vet_id: UUID, db: Session):
    vet = db.query(User).filter(User.id == vet_id).first()
    if not vet.role == "VET":
        raise HTTPException(status_code=404, detail="Vet not found")
    
    appointments = db.query(Appointment).filter(Appointment.vet_id == vet_id).all()
    return appointments

def get_all_owner_appointments(owner_id: UUID, db: Session):
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")
    
    appointments = db.query(Appointment).filter(Appointment.owner_id == owner_id).all()
    return appointments

def update_appointment_status(appointment_id: UUID, status: str, db: Session):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment.status = status
    db.commit()
    db.refresh(appointment)
    return appointment