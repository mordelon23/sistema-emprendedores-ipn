from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.report import Report
from app.models.publication import Publication
from app.models.comment import Comment
from app.schemas.report import ReportCreate, ReportResponse
from app.utils.security import get_current_user, require_admin

router = APIRouter(prefix="/api/reports", tags=["Reportes"])


@router.post("/", response_model=ReportResponse, status_code=201)
def crear_reporte(
    datos: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if datos.publication_id:
        pub = db.query(Publication).filter(Publication.id == datos.publication_id).first()
        if not pub:
            raise HTTPException(status_code=404, detail="Publicación no encontrada")
    if datos.comment_id:
        com = db.query(Comment).filter(Comment.id == datos.comment_id).first()
        if not com:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")

    nuevo = Report(
        reportador_id=current_user.id,
        publication_id=datos.publication_id,
        comment_id=datos.comment_id,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=List[ReportResponse])
def listar_reportes(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(Report).filter(Report.resolved == False).order_by(Report.created_at.desc()).all()


@router.put("/{report_id}/resolve", status_code=204)
def resolver_reporte(
    report_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    rep = db.query(Report).filter(Report.id == report_id).first()
    if not rep:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    rep.resolved = True
    db.commit()