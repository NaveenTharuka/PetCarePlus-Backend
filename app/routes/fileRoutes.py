from fastapi import UploadFile
import app.services.petServices
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
from app.model.user import UserOut
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

@router.delete("/pet/report/{report_id}/delete")
async def delete_report(report_id : UUID , db : Session = Depends(get_db)):
    return await UploadServices.delete_pet_report(report_id, db)

@router.get("/pet/report/{report_id}/download", response_model=str)
def get_download_link(report_id :UUID , db : Session = Depends(get_db)):
    return UploadServices.get_report_download_link(report_id, db)

@router.post("/user/{user_id}/profile/upload", response_model=UserOut)
async def upload_user_profile_pic(user_id:UUID,file:UploadFile=File(...),db:Session = Depends(get_db)):
    return await UploadServices.upload_user_profile_picture(user_id, file, db)