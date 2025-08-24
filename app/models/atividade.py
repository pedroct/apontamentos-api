from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func
from app.db.base import Base


class Atividade(Base):
    __tablename__ = "atividades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, server_default="true")
    criado_em = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
