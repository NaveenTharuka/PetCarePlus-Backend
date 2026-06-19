from fastapi import APIRouter
import app.services.vetVisitsServices as visitService
from app.model.vetVisits import vetVisitCreate , vetVisitOut
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException , Depends


router = APIRouter()

@router.post("/visits/create",response_model=vetVisitOut)
def create_vet_visit(visit: vetVisitCreate , db:Session = Depends(get_db)):
    return visitService.create_vet_visit(visit,db)

@router.get("/visits/pet/{pet_id}",response_model=list[vetVisitOut])
def get_vet_visit(pet_id:UUID , db:Session = Depends(get_db)):
    return visitService.get_vet_visit(pet_id,db)

@router.get("/visits/{visit_id}",response_model=vetVisitOut)
def get_vet_visit_by_id(visit_id:UUID , db:Session = Depends(get_db)):
    return visitService.get_vet_visit_by_id(visit_id,db)