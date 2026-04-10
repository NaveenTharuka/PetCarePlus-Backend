from app.model.pet import PetOut
from app.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.model.user import UserOut
from app.database_models import Pet

router = APIRouter()

@router.get("/pets", response_model=list[PetOut])
def get_all_pets(db: Session = Depends(get_db)):
    pets = db.query(Pet).all()
    return pets