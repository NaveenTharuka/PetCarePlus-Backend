from fastapi import HTTPException
from app.database_models import Pet, Vaccination
from sqlalchemy.orm.session import Session
from app.model.vaccination import VaccinationCreate, VaccinationEdit
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

def delete_vaccine(vax_id : UUID, db: Session):
    db_vax = db.query(Vaccination).filter(Vaccination.id == vax_id).first()
    if not db_vax:
        raise HTTPException(status_code=404, detail="Vaccination Not Found")
    db.delete(db_vax)
    db.commit()
    return {"message": "Vaccination deleted successfully"}

def get_vaccine_by_id(vax_id : UUID, db: Session):
    db_vax = db.query(Vaccination).filter(Vaccination.id == vax_id).first()
    if not db_vax:
        raise HTTPException(status_code=404, detail="Vaccination Not Found")
    return db_vax

def update_vaccine(vax_id : UUID, pet_vaccine : VaccinationEdit, db: Session):
    db_vax = db.query(Vaccination).filter(Vaccination.id == vax_id).first()
    if not db_vax:
        raise HTTPException(status_code=404, detail="Vaccination Not Found")
    
    if pet_vaccine.vaccineName:
        db_vax.vaccine_name = pet_vaccine.vaccineName
    if pet_vaccine.vaccineDate:
        db_vax.vaccine_date = pet_vaccine.vaccineDate
    if pet_vaccine.vetName:
        db_vax.vet_name = pet_vaccine.vetName
    if pet_vaccine.dueDate:
        db_vax.next_due_date = pet_vaccine.dueDate
    if pet_vaccine.notes:
        db_vax.notes = pet_vaccine.notes
    
    db.commit()
    db.refresh(db_vax)
    return db_vax

    