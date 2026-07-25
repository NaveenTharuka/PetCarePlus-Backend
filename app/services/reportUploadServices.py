from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from uuid import uuid4, UUID
from enum import Enum
import os

from app.database_models import Pet, Report, ProfilePictures, User
from app.services import storage as StorageServices, notificationServices
from app.supabase import supabase

SUPABASE_URL = os.getenv("SUPABASE_URL")
BUCKET = "PetCarePlus"

# Add enum for clarity
class EntityType(str, Enum):
    USER = "user"
    PET = "pet"


def get_public_url(file_path: str) -> str:
    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{file_path}"


async def upload_report(
    pet_id: UUID, 
    file: UploadFile, 
    title: str, 
    db: Session
) -> Report:
    """Upload a medical report for a pet."""
    
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # Generate filename
    file_ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "bin"
    filename = f"{uuid4()}-{title}.{file_ext}"
    
    # Upload file
    storage_path = await StorageServices.upload_file(
        file=file,
        file_name=filename,
        folder="MedicalReports"
    )
    
    # Create report
    report = Report(
        title=title,
        file_path=storage_path,
        pet_id=pet_id,
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    # Add public URL for response
    report.file_url = get_public_url(storage_path)
    
    notification = notificationServices.create_report_notification(report, db)
    await notificationServices.create_notification(notification, db)

    return report


async def upload_pet_picture(
    pet_id: UUID, 
    file: UploadFile, 
    db: Session
) -> Pet:
    """Upload a profile picture for a pet."""
    
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # Delete old picture if exists
    if pet.profile_pic_id:
        await delete_profile_picture(db, pet.profile_pic_id, EntityType.PET)
    
    # Upload new picture
    filename = f"PetPhoto-{pet_id}"
    storage_path = await StorageServices.upload_file(
        file=file,
        file_name=filename,
        folder="ProfilePhotosPet"
    )
    
    # Create profile picture record
    profile_picture = ProfilePictures(
        pet_id=pet_id,
        file_path=storage_path,
        name=filename,
    )
    
    # Update pet with public URL
    pet.image_url = get_public_url(storage_path)
    
    db.add(pet)
    db.add(profile_picture)
    db.commit()
    db.refresh(pet)
    
    return pet


async def upload_user_profile_picture(
    user_id: UUID, 
    file: UploadFile, 
    db: Session
) -> User:
    """Upload a profile picture for a user."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete old picture if exists
    if user.profile_pic_id:
        await delete_profile_picture(db, user.profile_pic_id, EntityType.USER)
    
    # Upload new picture
    filename = f"UserPhoto-{user_id}"
    storage_path = await StorageServices.upload_file(
        file=file,
        file_name=filename,
        folder="ProfilePhotosUser"
    )
    
    # Create profile picture record
    profile_picture = ProfilePictures(
        user_id=user_id,
        file_path=storage_path,
        name=filename,
    )
    
    # Update user with public URL
    user.image_url = get_public_url(storage_path)

    db.add(profile_picture)
    db.commit()
    db.refresh(profile_picture)

    user.profile_pic_id = profile_picture.id  # FIX: Link the picture to user
    
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


async def delete_profile_picture(
    db: Session, 
    profile_picture_id: UUID, 
    entity_type: EntityType
) -> dict:
    """Delete a profile picture from storage and database."""
    
    # Find the profile picture
    profile_picture = db.query(ProfilePictures).filter(
        ProfilePictures.id == profile_picture_id
    ).first()
    
    if not profile_picture:
        return
    
    # Delete from storage
    storage_path = profile_picture.file_path
    result = supabase.storage.from_(BUCKET).remove([storage_path])
    
    # Delete from database
    db.delete(profile_picture)
    db.commit()
    
    return {
        "deleted_storage": result,
        "deleted_db": True,
        "entity_type": entity_type.value
    }


async def delete_pet_report(
    report_id: UUID,  # Changed to UUID for consistency
    db: Session
) -> dict:
    """Delete a pet report from storage and database."""
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Delete from storage
    result = supabase.storage.from_(BUCKET).remove([report.file_path])
    
    # Delete from database
    db.delete(report)
    db.commit()
    
    return {
        "deleted_storage": result,
        "deleted_db": True
    }


def get_report_download_link(report_id: UUID, db: Session) -> str:
    """Get public download link for a report."""
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return get_public_url(report.file_path)