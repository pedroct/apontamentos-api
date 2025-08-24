# app/routers/atividades.py
from fastapi import APIRouter, Depends, Query, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.atividade import Atividade
from app.schemas.atividade import AtividadeIn, AtividadeOut
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/atividades", tags=["atividades"])


# --- Alias sem barra final para evitar 307 em /api/atividades ---
@router.get("", include_in_schema=False)
def listar_alias(
    somente_ativas: bool = Query(False),
    q: str | None = Query(None),
    order_desc: bool = Query(True),
    db: Session = Depends(get_db),
):
    return listar_atividades(somente_ativas, q, order_desc, db)


# --- Listagem simples (retrocompatível) ---
@router.get("/", response_model=list[AtividadeOut])
def listar_atividades(
    somente_ativas: bool = Query(
        False, description="Se true, retorna apenas ativo=true"
    ),
    q: str | None = Query(None, description="Filtro de nome (ILIKE)"),
    order_desc: bool = Query(True, description="Ordenação por criado_em (desc padrão)"),
    db: Session = Depends(get_db),
):
    query = db.query(Atividade)
    if somente_ativas:
        query = query.filter(Atividade.ativo.is_(True))
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(Atividade.nome.ilike(like))
    query = query.order_by(
        Atividade.criado_em.desc() if order_desc else Atividade.criado_em.asc()
    )
    return query.all()


# --- Tipos para paginação ---
class PageInfo(BaseModel):
    page: int
    page_size: int
    total: int


class AtividadePage(BaseModel):
    items: list[AtividadeOut]
    page_info: PageInfo


# --- Listagem paginada ---
@router.get("/paged", response_model=AtividadePage)
def listar_atividades_paginado(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    somente_ativas: bool = Query(False),
    q: str | None = Query(None),
    order_desc: bool = Query(True),
    db: Session = Depends(get_db),
):
    base = db.query(Atividade)
    if somente_ativas:
        base = base.filter(Atividade.ativo.is_(True))
    if q:
        like = f"%{q.strip()}%"
        base = base.filter(Atividade.nome.ilike(like))

    # Contagem correta via subselect para evitar duplicações
    subq = base.with_entities(Atividade.id).subquery()
    total = db.query(func.count()).select_from(subq).scalar()

    query = base.order_by(
        Atividade.criado_em.desc() if order_desc else Atividade.criado_em.asc()
    )
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": items,
        "page_info": PageInfo(page=page, page_size=page_size, total=total),
    }


# --- Criação ---
@router.post("/", response_model=AtividadeOut, status_code=status.HTTP_201_CREATED)
def criar_atividade(payload: AtividadeIn, db: Session = Depends(get_db)):
    # normaliza o nome para evitar conflitos por espaços
    nome = payload.nome.strip()

    obj = Atividade(nome=nome, descricao=payload.descricao, ativo=payload.ativo)
    db.add(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Postgres: 23505 = unique_violation
        if getattr(getattr(e, "orig", None), "sqlstate", None) == "23505":
            raise HTTPException(status_code=409, detail="atividade_nome_ja_existe")
        # outras integridade → propaga
        raise
    db.refresh(obj)
    return obj
