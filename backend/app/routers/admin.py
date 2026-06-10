from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.sanction import Sanction
from app.schemas.user import UserResponse
from app.schemas.sanction import SanctionCreate, SanctionResponse
from app.utils.security import require_admin

router = APIRouter(prefix="/api/admin", tags=["Administración"])


@router.get("/users", response_model=List[UserResponse])
def listar_usuarios(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).all()


@router.delete("/users/{user_id}", status_code=204)
def eliminar_usuario(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()


@router.put("/users/{user_id}/promote", response_model=UserResponse)
def promover_admin(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.is_admin = True
    db.commit()
    db.refresh(user)
    return user


@router.post("/sanctions", response_model=SanctionResponse, status_code=201)
def crear_sancion(
    datos: SanctionCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == datos.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    nueva = Sanction(
        user_id=datos.user_id,
        motivo=datos.motivo,
        expires_at=datetime.utcnow() + timedelta(days=datos.dias),
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.get("/sanctions", response_model=List[SanctionResponse])
def listar_sanciones(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(Sanction).filter(Sanction.expires_at > datetime.utcnow()).all()