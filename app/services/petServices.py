from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services import notificationServices

from app.database_models import Pet, User
from app.model.pet import PetCreate, PetEdit

# 🔹 Create pet
async def create_pet(user_id: UUID, pet: PetCreate, db: Session):
    pet_owner = db.query(User).filter(User.id == user_id).first()

    if not pet_owner:
        raise HTTPException(status_code=404, detail="User not found")

    db_pet = Pet(
        name=pet.name,
        species=pet.species,
        breed=pet.breed,
        date_of_birth=pet.date_of_birth,
        weight=pet.weight,
        colour=pet.colour,
        is_registered=pet.is_registered,
        gender=pet.gender,
        owner_id=user_id
    )

    try:
        db.add(db_pet)
        db.commit()
        db.refresh(db_pet)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    pet_notification = notificationServices.create_pet_notification(db_pet)
    await notificationServices.create_notification(pet_notification,db)

    return db_pet


# 🔹 Get pets by user
def get_pets_by_user_id(user_id: UUID, db: Session):
    return db.query(Pet).filter(Pet.owner_id == user_id).all()


# 🔹 Get single pet
def get_pet_by_id(pet_id: UUID, db: Session):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    return pet


# 🔹 Get all pets
def get_all_pets(db: Session):
    return db.query(Pet).all()


# 🔹 Delete pet
def delete_pet(pet_id: UUID, db: Session):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    if pet.profile_pic_id:
        delete_profile_pic(db, pet.profile_pic_id,"PET")

    db.delete(pet)
    db.commit()

    return {"message": "Pet deleted successfully"}


# 🔹 Edit pet (partial update)
def edit_pet(pet_id: UUID, pet: PetEdit, db: Session):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    update_data = pet.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_pet, key, value)

    try:
        db.commit()
        db.refresh(db_pet)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return db_pet