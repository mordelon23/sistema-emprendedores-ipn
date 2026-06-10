from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.publication import CategoriaEnum


class PublicationBase(BaseModel):
    titulo: str
    descripcion: str
    precio: float
    contacto: str
    categoria: CategoriaEnum


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    contacto: Optional[str] = None
    categoria: Optional[CategoriaEnum] = None


class PublicationResponse(PublicationBase):
    id: int
    user_id: int
    imagen_url: Optional[str]
    created_at: datetime
    expires_at: datetime
    vendedor_nombre: Optional[str] = None
    vendedor_apellido: Optional[str] = None

    class Config:
        from_attributes = True