from sqlalchemy.orm import Session
from app.database_models import Pet
from fastapi import HTTPException
from app.database_models import Report
import app.services.storage

StorageServices = app.services.storage

async def upload_report(pet_id, file, title, db : Session):
    
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    file_path = await StorageServices.upload_file(file, title)

    db_report = Report(
        title = title,
        file_path = file_path,
        pet_id = pet_id
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return db_report