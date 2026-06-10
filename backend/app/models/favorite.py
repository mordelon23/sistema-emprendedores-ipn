from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("comprador_id", "emprendedor_id", name="unique_favorite"),)

    id = Column(Integer, primary_key=True, index=True)
    comprador_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    emprendedor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    comprador = relationship("User", foreign_keys=[comprador_id], back_populates="favorites_made")
    emprendedor = relationship("User", foreign_keys=[emprendedor_id], back_populates="favorited_by")