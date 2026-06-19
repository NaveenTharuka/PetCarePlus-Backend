from pydantic import BaseModel, ConfigDict, field_serializer
from uuid import UUID
from datetime import datetime

class ReportCreate(BaseModel):
    title : str

class ReportOut(ReportCreate):
    id : UUID
    file_path : str
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at")
    def format_created_at(self, value: datetime):
        return value.strftime("%b %d, %Y")