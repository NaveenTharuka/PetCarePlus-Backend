from app.model.pet import PetOut
from app.model.pet import PetEdit
from uuid import UUID
from app.model.pet import PetCreate
from app.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database_models import Pet, User
from fastapi import HTTPException


# Add a pet
def create_pet(user_id : UUID, pet: PetCreate, db : Session):
    pet_owner = db.query(User).filter(User.id == user_id).first()

    if not pet_owner:
        raise HTTPException(status_code=404, detail="User not found")

    db_pet = Pet(
        name = pet.name,
        species = pet.species,
        breed = pet.breed,
        colour = pet.colour,
        isRegistered = pet.isRegistered,
        owner_id = user_id
    )
    try:
        db.add(db_pet)
        db.commit()
        db.refresh(db_pet)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return db_pet


# Get pets
def getPetsByUser_id(user_id : UUID, db : Session):
    pets = db.query(Pet).filter(Pet.owner_id == user_id).all()
    if not pets:
        raise HTTPException(status_code=404, detail="Pets not found")
    return pets

def getPetBy_id(pet_id : UUID, db : Session):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

def getAllPets(db : Session):
    pets = db.query(Pet).all()
    return pets


# Delete pets
def deletePet(pet_id : UUID, db : Session):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    return HTTPException(status_code=200, detail="Pet deleted successfully")


# Edit pet
def editPet(pet_id : UUID, pet : PetEdit, db : Session):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    db_pet.name = pet.name
    db_pet.species = pet.species
    db_pet.breed = pet.breed
    db_pet.colour = pet.colour
    db_pet.isRegistered = pet.isRegistered

    try:
        db.commit()
        db.refresh(db_pet)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return HTTPException(status_code=200, detail=PetOut.model_validate(db_pet))