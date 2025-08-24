from datetime import datetime
from pydantic import BaseModel, Field


class AtividadeIn(BaseModel):
    nome: str = Field(min_length=1, max_length=255)
    descricao: str | None = None
    ativo: bool = True


class AtividadeOut(AtividadeIn):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
