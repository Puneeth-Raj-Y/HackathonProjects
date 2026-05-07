from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import logging
from pathlib import Path

# Configure logging FIRST
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("forgemind.api")

logger.info("=" * 80)
logger.info("STARTING FORGEMIND AI API INITIALIZATION")
logger.info("=" * 80)

# Initialize database
try:
    from database.db import engine, Base
    logger.info("Database module imported successfully")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database initialized successfully")
except Exception as e:
    logger.error(f"✗ Database initialization failed: {e}", exc_info=True)
    sys.exit(1)

# Initialize NLP engine
try:
    from nlp.engine import nlp_engine
    logger.info("✓ NLP engine initialized successfully")
except Exception as e:
    logger.error(f"✗ NLP engine initialization failed: {e}", exc_info=True)
    logger.warning("Continuing without NLP engine (fallback mode)")

# Import routers after dependencies are initialized
try:
    from routes import orders, chat
    logger.info("✓ API routes imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import routes: {e}", exc_info=True)
    sys.exit(1)

# Create FastAPI application
app = FastAPI(
    title="ForgeMind AI API",
    description="AI-powered enterprise workflow platform",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("✓ CORS middleware configured")

# Include routers
app.include_router(orders.router)
app.include_router(chat.router)
logger.info("✓ API routers included")

# Health check endpoint
@app.get("/api/health")
def health_check():
    """Production health monitoring endpoint"""
    try:
        from sqlalchemy import text
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

# Frontend serving
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

if FRONTEND_DIST.exists():
    logger.info(f"✓ Frontend build found at {FRONTEND_DIST}")
    
    # Mount assets
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
        logger.info("✓ Assets mounted")
    
    # SPA fallback route
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve SPA with fallback to index.html"""
        # Don't intercept API calls
        if full_path.startswith("api/"):
            return JSONResponse({"error": "Not Found"}, status_code=404)
        
        # Try to serve static file
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file() and full_path:
            return FileResponse(str(file_path))
        
        # Fallback to index.html for SPA routing
        return FileResponse(str(FRONTEND_DIST / "index.html"))
else:
    logger.warning(f"Frontend build not found at {FRONTEND_DIST}")
    logger.warning("API will be available but frontend will not be served")

logger.info("=" * 80)
logger.info("INITIALIZATION COMPLETE - API READY")
logger.info("=" * 80)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
