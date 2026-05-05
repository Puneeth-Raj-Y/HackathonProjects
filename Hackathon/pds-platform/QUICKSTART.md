# PDS Platform - Quick Start Guide

Get the platform running in 5 minutes!

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
cd pds-platform
pip install -r requirements.txt
```

### 2. Train ML Model (2 minutes)
```bash
cd backend/ml/scripts
python train_model.py
```
✓ Creates: `backend/ml/models/fraud_detection_model.pkl`

### 3. Generate Sample Data (1 minute)
```bash
python generate_sample_data.py
```
✓ Creates: Database with 20+ test users, warehouses, shops

### 4. Start Backend Server
```bash
cd ../../
python app.py
```

**Output:**
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### 5. Access the Platform

- **API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health

---

## 🧪 Quick Testing

### Using Demo Credentials

**Admin Login**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"unique_id":"ADMIN123456","password":"admin_pass"}'
```

**Response**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "role": "admin",
  "name": "System Admin"
}
```

### Make Your First API Call

Save the token from login, then:

```bash
TOKEN="<your_token_here>"

curl -X GET http://localhost:5000/api/stock/warehouses \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎯 User Flows

### Admin Workflow
1. Login with `ADMIN123456 / admin_pass`
2. View fraud dashboard
3. Add warehouses
4. Create shops
5. Monitor transactions
6. Review grievances

### Shop Manager Workflow
1. Login with `SHOP000000 / shop_pass`
2. View inventory
3. Request stock
4. Distribute goods to beneficiaries
5. Check fraud alerts

### Beneficiary Workflow
1. Login with `BENEFICIARY000000 / beneficiary_pass`
2. View distribution history
3. File grievance
4. Track complaint status

---

## 📊 Sample Data Created

```
✓ 1 Admin user
✓ 3 Warehouses with locations
✓ 6 Shops linked to warehouses
✓ 20 Beneficiary users
✓ 3 Shop managers
✓ 60+ Stock transactions
✓ 80+ Beneficiary distributions
✓ 10+ Grievances
```

---

## 🔍 Test Fraud Detection

### Normal Distribution
```bash
TOKEN="<your_token>"

curl -X POST http://localhost:5000/api/transactions/distribute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "shop_id": 1,
    "quantity": 12.0
  }'
```

**Expected Response:**
```json
{
  "fraud_risk": {
    "is_fraud": false,
    "risk_score": 0.15,
    "reason": "ML: Normal transaction | Rules: No rule violations",
    "confidence": "low"
  }
}
```

### High-Risk Distribution
```bash
curl -X POST http://localhost:5000/api/transactions/distribute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "shop_id": 1,
    "quantity": 200.0
  }'
```

**Expected Response:**
```json
{
  "fraud_risk": {
    "is_fraud": true,
    "risk_score": 0.78,
    "reason": "ML: Anomaly detected (score: 0.85) | Rules: High quantity: 200.0 exceeds max 50.0",
    "confidence": "high"
  }
}
```

---

## 📁 Key Files to Know

| File | Purpose |
|------|---------|
| `backend/app.py` | Main Flask entry point |
| `backend/src/models/__init__.py` | Database models |
| `backend/src/routes/*.py` | API endpoints |
| `backend/ml/fraud_detector.py` | Fraud detection engine |
| `backend/ml/models/fraud_detection_model.pkl` | Trained ML model |
| `frontend/templates/*.html` | UI dashboards |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'sklearn'"
**Fix:** Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Database locked"
**Fix:** Delete old database
```bash
rm pds_platform.db
```

### Problem: "Port 5000 already in use"
**Fix:** Check what's running, or use different port in `backend/app.py`
```python
app.run(port=5001)
```

### Problem: "Model not found"
**Fix:** Train the model
```bash
cd backend/ml/scripts
python train_model.py
```

---

## 📞 Need Help?

1. **API Issues**: Check `README.md` for full API documentation
2. **Database Issues**: Delete `pds_platform.db` and restart
3. **Model Issues**: Re-run training script
4. **Data Issues**: Re-generate sample data

---

## 🚀 What's Next?

- [ ] Explore admin dashboard
- [ ] Test all role types
- [ ] Review fraud alerts
- [ ] Check API endpoints
- [ ] Read full documentation (README.md)
- [ ] Customize rules/thresholds

---

## 📈 Performance Test

Check API response times:

```bash
# Health check (should be < 10ms)
curl -w "\n%{time_total}s\n" http://localhost:5000/api/health

# Login (should be < 100ms)
curl -w "\n%{time_total}s\n" \
  -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"unique_id":"ADMIN123456","password":"admin_pass"}'
```

---

**You're all set! 🎉 Start exploring the PDS Platform**

For detailed documentation, see: `README.md`
