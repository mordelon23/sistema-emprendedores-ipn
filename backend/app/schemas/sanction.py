from pydantic import BaseModel
from datetime import datetime


class SanctionCreate(BaseModel):
    user_id: int
    motivo: str
    dias: int


class SanctionResponse(BaseModel):
    id: int
    user_id: int
    motivo: str
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True