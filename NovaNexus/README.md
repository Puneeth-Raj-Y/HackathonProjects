# ForgeMind AI - Deployment Guide

ForgeMind AI (formerly NovaNexus) is an enterprise-grade AI-powered Multi-Item Order Management System. It features a conversational intelligence engine that correctly parses complex inputs across multiple industries.

This repository is optimized for deployment on **Render.com**.

## Project Architecture
- **Frontend**: React (Vite), Framer Motion, TailwindCSS
- **Backend**: FastAPI, SQLite3, spaCy, SQLAlchemy

---

## 🚀 1. Frontend Deployment (Render Static Site)

1. Create a new **Static Site** on Render.
2. Connect this repository.
3. **Settings**:
   - **Root Directory**: `NovaNexus/frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. **Environment Variables**:
   - `VITE_API_URL` = `https://<your-backend-render-url>.onrender.com/api`
5. **Rewrite Rules** (For React Router support):
   - **Source**: `/*`
   - **Destination**: `/index.html`
   - **Action**: `Rewrite`

---

## 🚀 2. Backend Deployment (Render Web Service)

1. Create a new **Web Service** on Render.
2. Connect this repository.
3. **Settings**:
   - **Root Directory**: `NovaNexus/backend`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   - `PYTHON_VERSION` = `3.10` (or your preferred version)
5. **Database**: 
   - Uses SQLite out of the box. 
   - *(Note: Render free tier wipes the disk on restart. For persistent data, attach a Render Disk to `/opt/render/project/src/backend/` and set `SQLALCHEMY_DATABASE_URL = "sqlite:////opt/render/project/src/backend/nova_nexus.db"`)*.

---

## ⚕️ Health Check
The backend is equipped with a `/health` endpoint to monitor startup. 
Visit `https://<your-backend-url>.onrender.com/health` to verify:
```json
{
  "status": "online",
  "backend": "working",
  "database": "connected",
  "nlp_engine": "loaded"
}
```

## 🛠 Troubleshooting

- **CORS Errors**: Ensure `VITE_API_URL` is set correctly on the frontend without trailing slashes. The backend inherently allows all origins (`allow_origins=["*"]`) for hackathon flexibility.
- **spaCy Model Failures**: The NLP engine (`backend/nlp/engine.py`) has a built-in fallback. If the spaCy `en_core_web_sm` model is missing on the Render image, it automatically triggers `os.system("python -m spacy download en_core_web_sm")` to ensure a crash-free startup.
- **API Port Not Found**: Render automatically injects the `$PORT` environment variable. The `main.py` explicitly uses `int(os.environ.get("PORT", 10000))` to prevent port-binding failures.
