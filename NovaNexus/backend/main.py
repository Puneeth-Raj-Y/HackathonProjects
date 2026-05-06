from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders.router)
app.include_router(chat.router)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
