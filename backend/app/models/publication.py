from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum
from app.database import Base


class CategoriaEnum(str, enum.Enum):
    dulces = "dulces"
    comida = "comida"
    accesorios = "accesorios"
    materiales_electronicos = "materiales_electronicos"
    articulos_electronicos = "articulos_electronicos"
    otros = "otros"


def default_expires_at():
    return datetime.utcnow() + timedelta(hours=24)


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(String(1000), nullable=False)
    precio = Column(Float, nullable=False)
    contacto = Column(String(255), nullable=False)
    categoria = Column(Enum(CategoriaEnum), nullable=False)
    imagen_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=default_expires_at)

    owner = relationship("User", back_populates="publications")
    comments = relationship("Comment", back_populates="publication", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="publication", cascade="all, delete-orphan")