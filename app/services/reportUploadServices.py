from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import uuid4, UUID
import os

from app.database_models import Pet, Report
from app.services import storage as StorageServices
from app.supabase import supabase

SUPABASE_URL = os.getenv("SUPABASE_URL")
BUCKET = "PetCarePlus"


def get_public_url(file_path: str):
    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{file_path}"


async def upload_report(pet_id, file, title, db: Session):

    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    file_ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "bin"
    file_name = f"{uuid4()}-{title}.{file_ext}"

    storage_path = await StorageServices.upload_file(
        file=file,
        file_name=file_name,
        folder="MedicalReports"
    )

    # store RAW path (IMPORTANT FIX)
    db_report = Report(
        title=title,
        file_path=storage_path,
        pet_id=pet_id,
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # return with public URL (optional)
    db_report.file_url = get_public_url(storage_path)

    return db_report


async def upload_pet_picture(pet_id, file, db: Session):

    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    file_name = f"PetPhoto-{pet_id}"

    storage_path = await StorageServices.upload_file(
        file=file,
        file_name=file_name,
        folder="ProfilePhotosPet"
    )

    db_pet.image_url = get_public_url(storage_path)

    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)

    return db_pet


async def delete_pet_report(report_id: str, db: Session):

    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    storage_path = report.file_path

    result = supabase.storage.from_(BUCKET).remove([storage_path])

    if report:
        db.delete(report)
        db.commit()

    return {
        "deleted_storage": result,
        "deleted_db": True
    }


def get_report_download_link(id:UUID , db:Session):
    report = db.query(Report).filter(Report.id == id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return get_public_url(report.file_path)