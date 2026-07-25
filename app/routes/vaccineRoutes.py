from fastapi import APIRouter, Depends
from app.model.vaccination import VaccinationCreate, VaccinationOut, VaccinationEdit
from app.database import get_db
from sqlalchemy.orm.session import Session
from uuid import UUID
import app.services.vaccineServices

router = APIRouter()

VaccineServices = app.services.vaccineServices

@router.post("/pet/{pet_id}/vaccine/add", response_model=VaccinationOut)
async def pet_add_vaccination(pet_id : UUID, pet_vaccine : VaccinationCreate , db: Session = Depends(get_db)):
    return await VaccineServices.add_vaccine(pet_id, pet_vaccine, db)

@router.delete("/vaccine/delete/{vax_id}")
def delete_vaccine(vax_id : UUID, db: Session = Depends(get_db)):
    return VaccineServices.delete_vaccine(vax_id, db)

@router.get("/vaccine/get/{vax_id}", response_model=VaccinationOut)
def get_vaccine_by_id(vax_id : UUID, db: Session = Depends(get_db)):
    return VaccineServices.get_vaccine_by_id(vax_id, db)

@router.put("/vaccine/update/{vax_id}", response_model=VaccinationOut)
def update_vaccine(vax_id : UUID, pet_vaccine : VaccinationEdit, db: Session = Depends(get_db)):
    return VaccineServices.update_vaccine(vax_id, pet_vaccine, db)