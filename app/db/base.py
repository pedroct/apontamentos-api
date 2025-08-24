from sqlalchemy import MetaData

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)

try:
    # SQLAlchemy 2.x
    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        metadata = metadata

except ImportError:
    # fallback 1.x (não esperado, mas evita erro fora da venv)
    from sqlalchemy.orm import declarative_base

    Base = declarative_base(metadata=metadata)
