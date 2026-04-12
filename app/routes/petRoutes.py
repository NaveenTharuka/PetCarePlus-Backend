import app.services.pet_services

from fastapi import HTTPException
from uuid import UUID
from app.model.pet import PetOut, PetCreate, PetEdit
from app.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database_models import Pet

router = APIRouter()

PetServices = app.services.pet_services


@router.get("/pets", response_model=list[PetOut])
def get_all_pets(db: Session = Depends(get_db)):
    pets = PetServices.getAllPets(db)
    return pets

@router.get("/pets/{pet_id}", response_model=PetOut)
def get_pet_by_id(pet_id : UUID, db : Session = Depends(get_db)):
    pet = PetServices.getPetBy_id(pet_id, db)
    return pet

@router.get("/pets/user/{user_id}", response_model=list[PetOut])
def get_pets_by_user_id(user_id : UUID, db : Session = Depends(get_db)):
    pets = PetServices.getPetsByUser_id(user_id, db)
    return pets

@router.post("/pets/user/{user_id}", response_model=PetOut)
def create_pet(user_id : UUID, pet: PetCreate, db : Session = Depends(get_db)):

    db_pet = PetServices.create_pet(user_id, pet, db)

    try:
        db.add(db_pet)
        db.commit()
        db.refresh(db_pet)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return db_pet

@router.delete("/pets/delete/{pet_id}")
def delete_pet(pet_id : UUID , db : Session = Depends(get_db)):
    return PetServices.deletePet(pet_id, db)


@router.put("/pets/edit/{pet_id}")
def edit_pet(pet_id : UUID, pet : PetEdit, db : Session = Depends(get_db)):
    return PetServices.editPet(pet_id, pet, db)