from fastapi import HTTPException
from app.database_models import Pet, Vaccination
from sqlalchemy.orm.session import Session
from app.model.vaccination import VaccinationCreate
from uuid import UUID

def add_vaccine(pet_id : UUID, pet_vaccine : VaccinationCreate, db : Session):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet Not Found")

    vaccination = Vaccination(
        pet_id = pet_id,
        vaccine_name = pet_vaccine.vaccineName,
        vaccine_date = pet_vaccine.vaccineDate,
        vet_name = pet_vaccine.vetName,
        next_due_date = pet_vaccine.dueDate,
        notes = pet_vaccine.notes,
    )
    db_pet.vaccinations.append(vaccination)

    try:
        db.add(db_pet)
        db.commit()
        db.refresh(vaccination)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return vaccination