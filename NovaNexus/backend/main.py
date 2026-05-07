"""
ForgeMind AI - FastAPI Backend
Comprehensive API with SPA serving and deployment safety
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import logging
from pathlib import Path
from sqlalchemy import text

# ============================================================================
# LOGGING SETUP
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("forgemind.api")

logger.info("=" * 80)
logger.info("STARTING FORGEMIND AI API INITIALIZATION")
logger.info("=" * 80)

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================
try:
    from database.db import engine, Base
    logger.info("✓ Database module imported successfully")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database tables created/verified")
except Exception as e:
    logger.error(f"✗ Database initialization failed: {e}", exc_info=True)
    sys.exit(1)

# ============================================================================
# NLP ENGINE INITIALIZATION
# ============================================================================
try:
    from nlp.engine import nlp_engine
    logger.info("✓ NLP engine initialized successfully")
except Exception as e:
    logger.error(f"✗ NLP engine initialization failed: {e}", exc_info=True)
    logger.warning("Continuing without NLP engine (fallback mode)")

# ============================================================================
# ROUTE IMPORTS
# ============================================================================
try:
    from routes import orders, chat
    logger.info("✓ API routes imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import routes: {e}", exc_info=True)
    sys.exit(1)

# ============================================================================
# FASTAPI APPLICATION SETUP
# ============================================================================
app = FastAPI(
    title="ForgeMind AI API",
    description="AI-powered enterprise workflow platform",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# ============================================================================
# CORS MIDDLEWARE - CRITICAL FOR FRONTEND COMMUNICATION
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]  # Expose all response headers
)
logger.info("✓ CORS middleware configured")

# ============================================================================
# HEALTH CHECK ENDPOINT (CRITICAL FOR MONITORING)
# ============================================================================
@app.get("/api/health", tags=["health"])
def health_check():
    """Production health monitoring endpoint"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "failed"

    from nlp.engine import nlp
    nlp_status = "loaded" if nlp is not None else "not_loaded"

    return {
        "status": "online",
        "backend": "stable",
        "database": db_status,
        "nlp_engine": nlp_status,
        "api_routes": "working"
    }

# ============================================================================
# INCLUDE API ROUTERS (MUST BE BEFORE SPA CATCH-ALL)
# ============================================================================
app.include_router(orders.router)
app.include_router(chat.router)
logger.info("✓ API routers included (orders, chat)")

# ============================================================================
# FRONTEND SERVING (SPA STATIC FILES)
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

if FRONTEND_DIST.exists():
    logger.info(f"✓ Frontend build found at {FRONTEND_DIST}")
    
    # Mount assets directory
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
        logger.info("✓ Assets mounted at /assets")
else:
    logger.warning(f"Frontend build not found at {FRONTEND_DIST}")
    logger.warning("API will be available but frontend will not be served")

# ============================================================================
# SPA CATCH-ALL ROUTE (MUST BE LAST)
# ============================================================================
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa(full_path: str):
    """Serve SPA with fallback to index.html"""
    if not FRONTEND_DIST.exists():
        return JSONResponse({"error": "Frontend not available"}, status_code=503)
    
    # Try to serve static file
    file_path = FRONTEND_DIST / full_path
    if file_path.exists() and file_path.is_file() and full_path:
        return FileResponse(str(file_path))
    
    # Fallback to index.html for SPA routing
    index_path = FRONTEND_DIST / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    
    return JSONResponse({"error": "Frontend not found"}, status_code=404)

logger.info("=" * 80)
logger.info("INITIALIZATION COMPLETE - API READY")
logger.info("=" * 80)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
