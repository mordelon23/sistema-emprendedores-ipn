from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.comment import Comment
from app.models.publication import Publication
from app.schemas.comment import CommentCreate, CommentResponse
from app.utils.security import get_current_user, check_active_sanction

router = APIRouter(prefix="/api/comments", tags=["Comentarios"])


def comment_to_response(c: Comment) -> CommentResponse:
    item = CommentResponse.from_orm(c)
    item.user_nombre = c.user.nombre
    item.user_apellido = c.user.apellido
    return item


@router.get("/publication/{publication_id}", response_model=List[CommentResponse])
def listar_comentarios(publication_id: int, db: Session = Depends(get_db)):
    comentarios = (
        db.query(Comment)
        .filter(Comment.publication_id == publication_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return [comment_to_response(c) for c in comentarios]


@router.post("/publication/{publication_id}", response_model=CommentResponse, status_code=201)
def crear_comentario(
    publication_id: int,
    datos: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if check_active_sanction(db, current_user.id):
        raise HTTPException(status_code=403, detail="Tienes una sanción activa, no puedes comentar")

    pub = db.query(Publication).filter(Publication.id == publication_id).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    nuevo = Comment(
        publication_id=publication_id,
        user_id=current_user.id,
        contenido=datos.contenido,
        parent_id=datos.parent_id,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return comment_to_response(nuevo)


@router.delete("/{comment_id}", status_code=204)
def eliminar_comentario(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    com = db.query(Comment).filter(Comment.id == comment_id).first()
    if not com:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    if com.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No puedes eliminar este comentario")
    db.delete(com)
    db.commit()