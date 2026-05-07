import logging
import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from database.db import Base, SessionLocal, engine
from models import models as model_defs
from nlp.engine import nlp, nlp_engine
from routes.admin import router as admin_router
from routes.chat import router as chat_router
from routes.dashboard import router as dashboard_router
from routes.orders import router as orders_router
from services.order_service import ensure_seed_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("forgemind.api")

app = FastAPI(
    title="ForgeMind AI",
    version="1.0.0",
    description="Production AI workflow platform",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)


def initialize_database() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized")
    except Exception:
        logger.exception("Database initialization failed; continuing with degraded startup")


initialize_database()

try:
    with SessionLocal() as db:
        ensure_seed_data(db)
except Exception:
    logger.exception("Import-time seed initialization failed; continuing")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    logger.info("Starting ForgeMind AI backend")
    initialize_database()

    try:
        with SessionLocal() as db:
            ensure_seed_data(db)
            logger.info("Seed data ensured")
    except Exception:
        logger.exception("Seed data initialization failed; continuing")


@app.get("/api/health")
def health_check():
    database_state = "connected"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        logger.exception("Health check database probe failed")
        database_state = "failed"

    return {
        "status": "online",
        "database": database_state,
        "nlp": "loaded" if nlp is not None else "fallback",
    }


app.include_router(chat_router)
app.include_router(orders_router)
app.include_router(dashboard_router)
app.include_router(admin_router)


BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")


@app.get("/{path:path}", include_in_schema=False)
def spa_fallback(path: str):
    if path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    index_file = FRONTEND_DIST / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))

    return JSONResponse(status_code=404, content={"detail": "Frontend not built"})


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "10000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
