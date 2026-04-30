from fastapi import UploadFile
import app.services.pet_services
import app.services.vaccineServices
import app.services.storage
import app.services.reportUploadServices

from uuid import UUID
from fastapi import Form, File
from app.model.report import ReportOut
from app.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.model.pet import PetOut
router = APIRouter()

UploadServices = app.services.reportUploadServices

@router.post("/pet/{pet_id}/report/upload", response_model=ReportOut)
async def upload_report(
    pet_id: UUID,
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await UploadServices.upload_report(pet_id, file, title, db)

@router.post("/pet/{pet_id}/picture/upload", response_model=PetOut)
async def upload_pet_picture(pet_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await UploadServices.upload_pet_picture(pet_id, file, db)