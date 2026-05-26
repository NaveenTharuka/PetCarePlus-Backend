from sqlalchemy.orm import Session
from app.database_models import Pet
from fastapi import HTTPException
from app.database_models import Report
import app.services.storage
from uuid import uuid4
import os

StorageServices = app.services.storage

SUPABASE_URL = os.getenv("SUPABASE_URL")

IMG_URL =  SUPABASE_URL + "/storage/v1/object/public/PetCarePlus" 

async def upload_report(pet_id, file, title, db : Session):
    
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    file_name_prefix = uuid4()
    file_ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "bin"
    
    file_name = f"{file_name_prefix}.{file_ext}"

    file_path = await StorageServices.upload_file(file, file_name, "MedicalReports")

    db_report = Report(
        title = title,
        file_path = IMG_URL + file_path,
        pet_id = pet_id
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return db_report

async def upload_pet_picture(pet_id, file, db : Session):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    file_name = "PetPhoto-" + str(pet_id)

    file_path = await StorageServices.upload_file(file, file_name, "ProfilePhotosPet")
    db_pet.image_url = IMG_URL + file_path
    db.commit()
    db.refresh(db_pet)
    return db_pet