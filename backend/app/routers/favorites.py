from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.favorite import Favorite
from app.models.publication import Publication
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["Favoritos"])


@router.post("/publication/{publication_id}", status_code=201)
def dar_corazon(
    publication_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pub = db.query(Publication).filter(Publication.id == publication_id).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    if pub.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes dar corazón a tu propia publicación")

    existente = (
        db.query(Favorite)
        .filter(Favorite.comprador_id == current_user.id, Favorite.emprendedor_id == pub.user_id)
        .first()
    )
    if existente:
        return {"mensaje": "Este emprendedor ya está en tus favoritos"}

    nuevo = Favorite(comprador_id=current_user.id, emprendedor_id=pub.user_id)
    db.add(nuevo)
    db.commit()
    return {"mensaje": "Emprendedor agregado a favoritos"}


@router.delete("/emprendedor/{emprendedor_id}", status_code=204)
def quitar_favorito(
    emprendedor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    fav = (
        db.query(Favorite)
        .filter(Favorite.comprador_id == current_user.id, Favorite.emprendedor_id == emprendedor_id)
        .first()
    )
    if not fav:
        raise HTTPException(status_code=404, detail="No tienes a este emprendedor en favoritos")
    db.delete(fav)
    db.commit()