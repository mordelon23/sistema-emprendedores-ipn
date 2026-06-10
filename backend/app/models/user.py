from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    publications = relationship("Publication", back_populates="owner", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    favorites_made = relationship("Favorite", foreign_keys="Favorite.comprador_id", back_populates="comprador", cascade="all, delete-orphan")
    favorited_by = relationship("Favorite", foreign_keys="Favorite.emprendedor_id", back_populates="emprendedor", cascade="all, delete-orphan")
    reports_made = relationship("Report", back_populates="reportador", cascade="all, delete-orphan")
    sanctions = relationship("Sanction", back_populates="user", cascade="all, delete-orphan")