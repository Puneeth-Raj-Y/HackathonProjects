from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from database.db import engine, Base
from routes import orders, chat
from models import models

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("forgemind.api")

# Create database tables safely
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")

app = FastAPI(title="ForgeMind AI API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    """Production health monitoring endpoint"""
    db_status = "connected"
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "failed"

    from nlp.engine import nlp
    nlp_status = "loaded" if nlp is not None else "failed"

    return {
        "status": "online",
        "backend": "stable",
        "database": db_status,
        "nlp_engine": nlp_status,
        "api_routes": "working"
    }

# Include routers
app.include_router(orders.router)
app.include_router(chat.router)

# Mount frontend static files safely
dist_path = os.path.join(os.getcwd(), "frontend", "dist")
if os.path.exists(dist_path):
    logger.info(f"Mounting static files from {dist_path}")
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")
else:
    logger.warning(f"Static directory {dist_path} not found. Frontend skipped.")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    if os.path.exists(dist_path):
        return FileResponse(os.path.join(dist_path, "index.html"))
    return JSONResponse({"error": "Frontend build not found"}, status_code=404)

# Mount frontend
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(FRONTEND_PATH):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_PATH, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            return JSONResponse(status_code=404, content={"message": "API Not Found"})
        if os.path.exists(os.path.join(FRONTEND_PATH, full_path)) and full_path != "":
            return FileResponse(os.path.join(FRONTEND_PATH, full_path))
        return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))

if __name__ == "__main__":
    import uvicorn
    # Render assigns dynamic port via PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting uvicorn server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
