from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from database.db import engine, Base
from routes import orders, chat
from models import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ForgeMind AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders.router)
app.include_router(chat.router)

# Path to the frontend build directory
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

# Serve static files (CSS, JS)
if os.path.exists(FRONTEND_PATH):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_PATH, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Prevent catching API routes
        if full_path.startswith("api/"):
            return None # FastAPI will continue to search for other routes
        
        # Return index.html for all other routes to support React routing
        return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Welcome to Nova Nexus AI Manufacturing API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
