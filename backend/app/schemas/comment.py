from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    contenido: str
    parent_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    publication_id: int
    user_id: int
    contenido: str
    parent_id: Optional[int]
    created_at: datetime
    user_nombre: Optional[str] = None
    user_apellido: Optional[str] = None

    class Config:
        from_attributes = True