from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contenido = Column(String(500), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    publication = relationship("Publication", back_populates="comments")
    user = relationship("User", back_populates="comments")
    reports = relationship("Report", back_populates="comment", cascade="all, delete-orphan")
    replies = relationship("Comment", backref="parent", remote_side=[id])