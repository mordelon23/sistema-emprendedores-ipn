from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import os, uuid, aiofiles

from app.database import get_db
from app.models.user import User
from app.models.publication import Publication, CategoriaEnum
from app.schemas.publication import PublicationResponse, PublicationUpdate
from app.utils.security import get_current_user, check_active_sanction

router = APIRouter(prefix="/api/publications", tags=["Publicaciones"])

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def cleanup_expired(db: Session):
    """Borra publicaciones expiradas y sus imágenes."""
    expiradas = db.query(Publication).filter(Publication.expires_at < datetime.utcnow()).all()
    for pub in expiradas:
        if pub.imagen_url:
            ruta = pub.imagen_url.lstrip("/")
            if os.path.exists(ruta):
                try:
                    os.remove(ruta)
                except Exception:
                    pass
        db.delete(pub)
    db.commit()


def publication_to_response(p: Publication) -> PublicationResponse:
    item = PublicationResponse.from_orm(p)
    item.vendedor_nombre = p.owner.nombre
    item.vendedor_apellido = p.owner.apellido
    return item


@router.get("/", response_model=List[PublicationResponse])
def listar_publicaciones(
    categoria: Optional[CategoriaEnum] = None,
    db: Session = Depends(get_db),
):
    cleanup_expired(db)
    query = db.query(Publication).filter(Publication.expires_at > datetime.utcnow())
    if categoria:
        query = query.filter(Publication.categoria == categoria)
    publicaciones = query.order_by(Publication.created_at.desc()).all()
    return [publication_to_response(p) for p in publicaciones]


@router.get("/{publication_id}", response_model=PublicationResponse)
def obtener_publicacion(publication_id: int, db: Session = Depends(get_db)):
    cleanup_expired(db)
    pub = db.query(Publication).filter(Publication.id == publication_id).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return publication_to_response(pub)


@router.post("/", response_model=PublicationResponse, status_code=201)
async def crear_publicacion(
    titulo: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    contacto: str = Form(...),
    categoria: CategoriaEnum = Form(...),
    imagen: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if check_active_sanction(db, current_user.id):
        raise HTTPException(status_code=403, detail="Tienes una sanción activa, no puedes publicar")

    hace_24h = datetime.utcnow() - timedelta(hours=24)
    publicaciones_hoy = (
        db.query(Publication)
        .filter(Publication.user_id == current_user.id, Publication.created_at > hace_24h)
        .count()
    )
    if publicaciones_hoy >= 3:
        raise HTTPException(status_code=403, detail="Ya alcanzaste el límite de 3 publicaciones en 24 horas")

    imagen_url = None
    if imagen and imagen.filename:
        extension = os.path.splitext(imagen.filename)[1].lower()
        if extension not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(status_code=400, detail="Formato de imagen no permitido")
        nombre_archivo = f"{uuid.uuid4().hex}{extension}"
        ruta = os.path.join(UPLOAD_DIR, nombre_archivo)
        async with aiofiles.open(ruta, "wb") as f:
            contenido = await imagen.read()
            await f.write(contenido)
        imagen_url = f"/static/uploads/{nombre_archivo}"

    nueva_pub = Publication(
        user_id=current_user.id,
        titulo=titulo,
        descripcion=descripcion,
        precio=precio,
        contacto=contacto,
        categoria=categoria,
        imagen_url=imagen_url,
    )
    db.add(nueva_pub)
    db.commit()
    db.refresh(nueva_pub)
    return publication_to_response(nueva_pub)


@router.put("/{publication_id}", response_model=PublicationResponse)
def actualizar_publicacion(
    publication_id: int,
    datos: PublicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pub = db.query(Publication).filter(Publication.id == publication_id).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    if pub.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No puedes editar esta publicación")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(pub, campo, valor)
    db.commit()
    db.refresh(pub)
    return publication_to_response(pub)


@router.delete("/{publication_id}", status_code=204)
def eliminar_publicacion(
    publication_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pub = db.query(Publication).filter(Publication.id == publication_id).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    if pub.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No puedes eliminar esta publicación")
    if pub.imagen_url:
        ruta = pub.imagen_url.lstrip("/")
        if os.path.exists(ruta):
            try:
                os.remove(ruta)
            except Exception:
                pass
    db.delete(pub)
    db.commit()