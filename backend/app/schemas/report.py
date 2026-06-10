from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional


class ReportCreate(BaseModel):
    publication_id: Optional[int] = None
    comment_id: Optional[int] = None

    @model_validator(mode="after")
    def validar_uno_solo(self):
        if not self.publication_id and not self.comment_id:
            raise ValueError("Debes reportar una publicación o un comentario")
        if self.publication_id and self.comment_id:
            raise ValueError("Solo puedes reportar una publicación o un comentario, no ambos")
        return self


class ReportResponse(BaseModel):
    id: int
    reportador_id: int
    publication_id: Optional[int]
    comment_id: Optional[int]
    resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True