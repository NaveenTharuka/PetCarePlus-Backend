from fastapi import UploadFile
from app.model.vaccination import VaccinationCreate , VaccinationOut
import app.services.pet_services
import app.services.vaccineServices
import app.services.storage

from uuid import UUID
from app.model.pet import PetOut, PetCreate, PetEdit
from app.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

PetServices = app.services.pet_services
VaccineServices = app.services.vaccineServices
StorageServices = app.services.storage


@router.get("/pets", response_model=list[PetOut])
def get_all_pets(db: Session = Depends(get_db)):
    pets = PetServices.get_all_pets(db)
    return pets

@router.head("/pets", response_model=list[PetOut])
def get_all_pets(db: Session = Depends(get_db)):
    pets = PetServices.get_all_pets(db)
    return pets

@router.get("/pet/{pet_id}", response_model=PetOut)
def get_pet_by_id(pet_id : UUID, db : Session = Depends(get_db)):
    pet = PetServices.get_pet_by_id(pet_id, db)
    return pet

@router.get("/pets/user/{user_id}", response_model=list[PetOut])
def get_pets_by_user_id(user_id : UUID, db : Session = Depends(get_db)):
    pets = PetServices.get_pets_by_user_id(user_id, db)
    return pets

@router.post("/pets/user/{user_id}", response_model=PetOut)
async def create_pet(user_id : UUID, pet: PetCreate, db : Session = Depends(get_db)):

    db_pet = await PetServices.create_pet(user_id, pet, db)
    return db_pet
    

@router.delete("/pets/delete/{pet_id}" )
def delete_pet(pet_id : UUID , db : Session = Depends(get_db)):
    return PetServices.delete_pet(pet_id, db)


@router.put("/pets/edit/{pet_id}", response_model=PetOut)
def edit_pet(pet_id : UUID, pet : PetEdit, db : Session = Depends(get_db)):
    return PetServices.edit_pet(pet_id, pet, db)

