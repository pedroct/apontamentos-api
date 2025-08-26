# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

DATABASE_URL = getattr(settings, "DATABASE_URL", None)
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definido no ambiente (.env)")

# Engine e Session factory
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=Session,  # tipagem explícita (opcional)
)


# Dependency para FastAPI
def get_db():
    """
    Fornece uma sessão por request para ser injetada via Depends.
    Uso:
        def endpoint(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
