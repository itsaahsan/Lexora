import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

db_url = settings.DATABASE_URL
if db_url:
    db_url = db_url.strip().strip('"').strip("'")

# Serverless (Vercel) must not hold pooled connections across invocations:
# NullPool opens 1 short-lived connection per request and avoids pool
# checkout stalls + "too many clients" errors that make /register hang.
_is_serverless = bool(os.environ.get("VERCEL"))

try:
    if _is_serverless:
        engine = create_engine(
            db_url,
            poolclass=NullPool,
            pool_pre_ping=False,
            # NOTE: no "-c statement_timeout" in options — pooled hosts
            # (Neon pooler / pgbouncer) reject it as a startup parameter.
            connect_args={"connect_timeout": 5},
        )
    else:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=300,
            connect_args={"connect_timeout": 5},
        )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.warning(f"Could not create database engine: {e}")
    engine = None
    SessionLocal = None


class Base(DeclarativeBase):
    pass


def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
