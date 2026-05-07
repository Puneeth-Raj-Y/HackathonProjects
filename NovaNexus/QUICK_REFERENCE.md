# ForgeMind AI - Quick Reference & Deployment Checklist

## ⚡ Quick Start (Choose Your Path)

### Path 1: Test Locally First (5 min)
```bash
cd backend
pip install -r requirements.txt
python verify_deployment.py
# Expected: ✓ ALL CHECKS PASSED
```

### Path 2: Deploy Immediately
```bash
# 1. Build frontend
cd frontend && npm install && npm run build && cd ..

# 2. Push to GitHub
git add . && git commit -m "Ready for deployment" && git push

# 3. On Render - Create Web Service:
# Build: pip install -r backend/requirements.txt
# Start: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 📋 Pre-Deployment Checklist

### Code Quality
- [ ] Run `python backend/verify_deployment.py` - Should pass all checks
- [ ] No syntax errors: `python -c "import backend.main"`
- [ ] All imports work: Import test passed

### Backend Configuration
- [ ] `backend/runtime.txt` exists with `python-3.11.9`
- [ ] `backend/requirements.txt` includes spaCy model URL
- [ ] `backend/main.py` has been rebuilt (no duplicate functions)
- [ ] `backend/database/db.py` has environment detection

### Frontend Configuration
- [ ] `frontend/src/services/api.js` uses `window.location.origin`
- [ ] No hardcoded localhost in frontend code
- [ ] `npm run build` creates `frontend/dist/`

### Deployment Files
- [ ] `Procfile` exists and contains start command
- [ ] `.gitignore` includes `dist/`, `node_modules/`, `*.db`
- [ ] `verify_deployment.py` exists in backend

### Documentation
- [ ] `DEPLOYMENT.md` reviewed
- [ ] `NEXT_STEPS.md` reviewed
- [ ] `EXECUTIVE_SUMMARY.md` reviewed

---

## 🚀 Deployment Paths

### Render Web Service (Single Container)
**Recommended for simplicity**

Settings:
```
Root Directory: backend/
Build: pip install -r requirements.txt
Start: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Frontend served from `/` automatically.

### Render Web Service + Static Site (Separate)
**For advanced users**

Backend:
- Root: `backend/`
- Build: `pip install -r requirements.txt`
- Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

Frontend:
- Root: `frontend/`
- Build: `npm install && npm run build`
- Publish: `dist/`
- Env: `VITE_API_URL=https://backend-url.onrender.com`

---

## ✅ What Should Work After Deployment

### Health Check
```bash
curl https://[backend-url].onrender.com/api/health
# Response: {"status": "online", "database": "connected", ...}
```

### Chat
1. Frontend loads
2. Type message in chat
3. Gets AI response
4. Orders created in database

### Dashboard
1. Visit frontend
2. See customer/admin dashboard
3. Orders display correctly
4. Analytics show stats

### Refresh & Navigation
1. Refresh page → Data persists
2. Switch views → Works correctly
3. Click links → No 404 errors

---

## 🔧 API Endpoints Reference

```
GET /api/health
  └─ Check system status

POST /api/chat/
  ├─ Input: {"message": "...", "user_id": 1}
  └─ Output: {"reply": "...", "intent": "...", "extracted_data": {...}}

GET /api/orders/
  ├─ Query params: user_id, status
  └─ Output: List of orders

GET /api/orders/{id}
  └─ Output: Single order with details

PATCH /api/orders/{id}/status
  ├─ Query: status=new_status
  └─ Output: Confirmation

POST /api/orders/{id}/quality
  ├─ Query: note=quality_note
  └─ Output: Confirmation

GET /api/orders/analytics/summary
  └─ Output: {total_orders, pending, processing, completed, total_users}

GET /
  └─ Serves React SPA
```

---

## 🐛 Quick Troubleshooting

| Problem | Check | Fix |
|---------|-------|-----|
| Backend won't start | Render logs | Run verify_deployment.py locally |
| API 404 | Endpoint URL | Verify `/api/` prefix |
| Frontend blank | Browser console | Check VITE_API_URL setting |
| Chat fails | Network tab | Check /api/chat/ endpoint |
| Dashboard empty | API response | Ensure /api/orders/ returns data |
| Import error | Python version | Verify Python 3.11 via runtime.txt |

---

## 📊 File Manifest (What Was Changed)

### New Files (7)
- ✅ `backend/verify_deployment.py`
- ✅ `backend/__init__.py`
- ✅ `backend/runtime.txt` - Python 3.11.9
- ✅ `Procfile` - Render config
- ✅ `deploy.py` - Build helper
- ✅ `build.sh` - Unix helper
- ✅ All documentation (.md files)

### Modified Files (4)
- ✅ `backend/main.py` - Completely rebuilt
- ✅ `backend/database/db.py` - Render-aware paths
- ✅ `backend/routes/orders.py` - Added imports
- ✅ `frontend/src/services/api.js` - Smart URLs

### Unchanged (Still Working)
- ✓ `backend/nlp/engine.py` - Fixed imports, safe loading
- ✓ `backend/routes/chat.py`
- ✓ `backend/models/`
- ✓ `frontend/src/components/`
- ✓ `frontend/src/pages/`

---

## 🎯 Performance Targets

| Metric | Expected |
|--------|----------|
| Backend startup | 10-15 seconds (first time: +30s for spaCy) |
| API response | <500ms |
| Chat response | 1-3 seconds |
| Dashboard load | <2 seconds |
| Frontend build | 20-30 seconds |

---

## 🔐 Security Notes

Current setup:
```python
allow_origins=["*"]  # Development-friendly
```

For production, restrict to:
```python
allow_origins=["https://yourdomain.com"]
```

Edit in `backend/main.py` before production deployment.

---

## 📱 Browser Compatibility

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (responsive)

---

## 💾 Database Info

**Local Development**
- Type: SQLite
- File: `backend/forgemind.db` (auto-created)
- Persists: Yes

**Render Deployment**
- Type: SQLite
- File: `/tmp/forgemind.db` (auto-created)
- Persists: No (resets on restart)
- Note: For persistent data, attach Render Disk

---

## 📞 Getting Help

1. **Read**: `DEPLOYMENT.md` or `NEXT_STEPS.md`
2. **Check**: Render deployment logs
3. **Run**: `python backend/verify_deployment.py`
4. **Debug**: Check browser DevTools Network tab
5. **Review**: Backend logs for error details

---

## ✨ Features Included

- ✅ AI-powered order chatbot
- ✅ Multi-item order extraction
- ✅ Dashboard with analytics
- ✅ Role-based views (Customer/Admin)
- ✅ Real-time notifications
- ✅ Order tracking
- ✅ Quality logging
- ✅ Responsive UI
- ✅ Dark theme
- ✅ Smooth animations

---

## 🎉 Success Indicators

After deployment, you should see:

✅ Backend API responds to `/api/health`
✅ Frontend loads without errors
✅ Chat accepts messages
✅ Orders appear in dashboard
✅ Page refreshes preserve data
✅ Admin/Customer views switch
✅ Analytics display correctly
✅ No console errors

**If all these work → Deployment successful!**

---

## 📅 Version Info

- **Rebuild Date**: May 7, 2026
- **Python**: 3.11.9 (enforced)
- **Node**: 18+ (any recent)
- **Framework**: FastAPI + React
- **Status**: Production Ready

---

**Ready to deploy? Start with Step 1 in "Quick Start" above!**
