from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.favorite import Favorite
from app.models.publication import Publication
from app.schemas.user import UserResponse
from app.schemas.publication import PublicationResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/users", tags=["Usuarios"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.get("/{user_id}/publications", response_model=List[PublicationResponse])
def get_user_publications(user_id: int, db: Session = Depends(get_db)):
    from datetime import datetime
    publicaciones = (
        db.query(Publication)
        .filter(Publication.user_id == user_id, Publication.expires_at > datetime.utcnow())
        .order_by(Publication.created_at.desc())
        .all()
    )
    resultado = []
    for p in publicaciones:
        item = PublicationResponse.from_orm(p)
        item.vendedor_nombre = p.owner.nombre
        item.vendedor_apellido = p.owner.apellido
        resultado.append(item)
    return resultado


@router.get("/me/favorites", response_model=List[UserResponse])
def get_my_favorites(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    favoritos = db.query(Favorite).filter(Favorite.comprador_id == current_user.id).all()
    return [f.emprendedor for f in favoritos]