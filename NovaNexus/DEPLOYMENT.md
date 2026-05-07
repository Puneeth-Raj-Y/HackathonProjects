# ForgeMind AI Deployment Guide

## Quick Start

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python verify_deployment.py
uvicorn main:app --reload --port 10000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Production Deployment on Render

#### Step 1: Build Frontend
```bash
cd frontend
npm install
npm run build
```

This creates `frontend/dist/` with optimized production build.

#### Step 2: Push to GitHub
```bash
git add .
git commit -m "Production build"
git push
```

#### Step 3: Configure Render

1. Create new Web Service on Render
2. Connect your GitHub repository
3. Set Runtime: Python 3.11
4. Build Command:
```bash
pip install -r backend/requirements.txt && cd frontend && npm install && npm run build && cd ..
```

5. Start Command:
```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

6. Environment Variables:
   - `RENDER` = `true` (optional, for database path detection)

## Architecture

```
ForgeMind AI
├── Backend (FastAPI)
│   ├── main.py              - Application entry point
│   ├── database/            - SQLAlchemy setup
│   ├── models/              - Data models & schemas
│   ├── routes/              - API endpoints
│   ├── nlp/                 - NLP engine
│   ├── requirements.txt     - Python dependencies
│   └── runtime.txt          - Python version (3.11.9)
│
├── Frontend (React + Vite)
│   ├── src/
│   │   ├── services/api.js  - Axios configuration
│   │   ├── components/      - React components
│   │   └── pages/           - Page components
│   ├── package.json         - Dependencies
│   └── vite.config.js       - Build configuration
│
└── Procfile                 - Render deployment config
```

## API Endpoints

### Health & Status
- `GET /api/health` - System health check

### Chat
- `POST /api/chat/` - Send message to AI

### Orders
- `GET /api/orders/` - List orders
- `GET /api/orders/{id}` - Get order details
- `PATCH /api/orders/{id}/status` - Update order status
- `POST /api/orders/{id}/quality` - Add quality log
- `GET /api/orders/analytics/summary` - Get analytics

## Troubleshooting

### Backend Won't Start
1. Verify Python 3.11: `python --version`
2. Check imports: `python backend/verify_deployment.py`
3. Check database: SQLite permissions in `/tmp`
4. Check spaCy: Model installation in requirements.txt

### Frontend Not Loading
1. Verify build: `npm run build` creates `frontend/dist/`
2. Check base URL in `frontend/src/services/api.js`
3. Verify CORS in backend main.py

### API Calls Failing
1. Check health: `GET /api/health`
2. Verify API_URL in `frontend/src/services/api.js`
3. Check browser console for actual URLs being called
4. Verify backend logs for request processing

## Performance Notes

- Database: SQLite (ephemeral on Render)
- NLP Model: en_core_web_sm (loaded on startup)
- Frontend: React with Vite (optimized build)
- Deployment: Supports auto-scaling on Render

## Security

- CORS enabled for all origins (development-friendly)
- For production, restrict `allow_origins` in `backend/main.py`
- Use environment variables for sensitive data
- Database uses secure connection handling
