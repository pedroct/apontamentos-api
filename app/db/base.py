# app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# importe aqui seus modelos para o Alembic "enxergar" as tabelas:
# from app.models.example import Example  # noqa: F401
