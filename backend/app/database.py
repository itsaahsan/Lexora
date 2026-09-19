from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool
import os
from app.config import get_settings

settings = get_settings()

_db_url = settings.DATABASE_URL
if isinstance(_db_url, str):
    _db_url = _db_url.strip().strip('"').strip("'")

# Serverless (Vercel) must not hold pooled connections across invocations:
# NullPool opens 1 short-lived connection per request and avoids pool
# checkout stalls + "too many clients" errors that make /register hang.
# pool_pre_ping adds an extra SELECT 1 round-trip on every checkout, so we
# disable it on serverless where each request is a fresh connection anyway.
_is_serverless = bool(os.environ.get("VERCEL"))

if _is_serverless:
    engine = create_engine(
        _db_url,
        poolclass=NullPool,
        pool_pre_ping=False,
        connect_args={"connect_timeout": 5, "options": "-c statement_timeout=10000"},
    )
else:
    engine = create_engine(
        _db_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300,
        connect_args={"connect_timeout": 5},
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
