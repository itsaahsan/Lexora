import logging
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, Response, FileResponse
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, documents, chat, analytics, admin

settings = get_settings()

origins = list(settings.ALLOWED_ORIGINS)
if settings.FRONTEND_URL and settings.FRONTEND_URL not in origins:
    origins.append(settings.FRONTEND_URL)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"CORS allowed origins: {origins}")

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Lexora API...")
    try:
        if engine is not None:
            Base.metadata.create_all(bind=engine)
        else:
            logger.warning("Database engine not available, skipping table creation")
    except Exception as e:
        logger.warning(f"Database not available, skipping table creation: {e}")
    yield
    logger.info("Shutting down Lexora API...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    origin = request.headers.get("origin", "")
    headers = {
        "Access-Control-Allow-Origin": origin or "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Credentials": "true",
    }
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers=headers,
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["auth"])
app.include_router(documents.router, prefix=settings.API_V1_PREFIX, tags=["documents"])
app.include_router(chat.router, prefix=settings.API_V1_PREFIX, tags=["chat"])
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX, tags=["analytics"])
app.include_router(admin.router, prefix=settings.API_V1_PREFIX, tags=["admin"])


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION}


@app.get("/", include_in_schema=False)
def root():
    return JSONResponse({
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
        "api": settings.API_V1_PREFIX,
    })


@app.head("/", include_in_schema=False)
def head_root():
    return Response(status_code=200)


if settings.SERVE_FRONTEND and FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    @app.head("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")
