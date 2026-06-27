import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, documents, chat, analytics, admin

settings = get_settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Lexora API...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down Lexora API...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["auth"])
app.include_router(documents.router, prefix=settings.API_V1_PREFIX, tags=["documents"])
app.include_router(chat.router, prefix=settings.API_V1_PREFIX, tags=["chat"])
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX, tags=["analytics"])
app.include_router(admin.router, prefix=settings.API_V1_PREFIX, tags=["admin"])


@app.get("/")
@app.head("/")
async def root():
    return {"message": "Lexora API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION}
