from pydantic import BaseModel, ConfigDict
from uuid import UUID

class ReportCreate(BaseModel):
    title : str

class ReportOut(ReportCreate):
    id : UUID
    file_path : str
    model_config = ConfigDict(from_attributes=True)