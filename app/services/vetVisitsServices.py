from app.database_models import VetVisit, Pet
from app.database import get_db
from app.model.vetVisits import vetVisitCreate, vetVisitUpdate
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException

def create_vet_visit(visit: vetVisitCreate, db:Session):
    if not visit:
        raise HTTPException(status_code=400, detail="Invalid visit data")

    db_pet = db.query(Pet).filter(Pet.id == visit.pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    db_visit = VetVisit(
        pet_id = visit.pet_id,
        vet_name = visit.vet_name,
        visit_date = visit.visit_date,
        reason = visit.reason,
        note = visit.note
    )   
    
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

def get_vet_visit(pet_id:UUID,db:Session):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
        
    visits = db.query(VetVisit).filter(VetVisit.pet_id == pet_id).all()
    if not visits:
        raise HTTPException(status_code=404, detail="No visits found for this pet")
    return visits

def get_vet_visit_by_id(visit_id:UUID,db:Session):
    db_pet = db.query(Pet).filter(Pet.id == visit_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
        
    visit = db.query(VetVisit).filter(VetVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


def update_visit(pet_id:UUID, visit:vetVisitUpdate, db: Session):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    db_visit = db.query(VetVisit).filter(VetVisit.id == visit.visit_id).first()
    
    if not db_visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    updated_visit = visit.model_dump(exclude_unset=True)

    for key, value in updated_visit.items():
        setattr(db_visit, key, value)

    db.commit()
    db.refresh(db_visit)

    return db_visit

def delete_visit(visit_id:UUID,db:Session):
    db_visit = db.query(VetVisit).filter(VetVisit.id == visit_id).first()
    if not db_visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    db.delete(db_visit)
    db.commit()

    return {"message": "Visit deleted successfully"}