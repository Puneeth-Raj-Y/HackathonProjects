# PDS PLATFORM - API TESTING GUIDE & EXAMPLES

## Complete API Reference with cURL Examples

---

## 🔐 AUTHENTICATION ENDPOINTS

### 1. Register New User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "unique_id": "NEWUSER12345",
    "password": "secure_password_123",
    "role": "beneficiary"
  }'

# Response:
{
  "message": "User registered successfully",
  "user_id": 25,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "role": "beneficiary"
}
```

### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "unique_id": "ADMIN123456",
    "password": "admin_pass"
  }'

# Response:
{
  "message": "Login successful",
  "user_id": 1,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "role": "admin",
  "name": "System Admin"
}
```

### 3. Verify Token
```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X POST http://localhost:5000/api/auth/verify-token \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "message": "Token is valid",
  "user_id": 1,
  "role": "admin"
}
```

---

## 📦 STOCK MANAGEMENT ENDPOINTS

### 4. Get All Warehouses
```bash
curl -X GET http://localhost:5000/api/stock/warehouses

# Response:
{
  "count": 3,
  "warehouses": [
    {
      "id": 1,
      "name": "Central Warehouse",
      "location": "New Delhi",
      "created_at": "2024-01-15T10:30:00"
    },
    {
      "id": 2,
      "name": "North Warehouse",
      "location": "Punjab",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### 5. Add New Warehouse (Admin Only)
```bash
TOKEN="admin_token_here"

curl -X POST http://localhost:5000/api/stock/add-warehouse \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "West Warehouse",
    "location": "Gujarat"
  }'

# Response:
{
  "message": "Warehouse added successfully",
  "warehouse_id": 4
}
```

### 6. Add Stock to Warehouse (Admin Only)
```bash
TOKEN="admin_token_here"
WAREHOUSE_ID=1

curl -X POST http://localhost:5000/api/stock/warehouse/$WAREHOUSE_ID/add-stock \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 2000.0,
    "notes": "Monthly government supply"
  }'

# Response:
{
  "message": "Stock added successfully",
  "transaction_id": 50,
  "quantity": 2000.0
}
```

### 7. Dispatch Stock to Shop
```bash
TOKEN="admin_token_here"
WAREHOUSE_ID=1

curl -X POST http://localhost:5000/api/stock/warehouse/$WAREHOUSE_ID/dispatch \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "shop_id": 1,
    "quantity": 500.0
  }'

# Response:
{
  "message": "Stock dispatched successfully",
  "transaction_id": 51,
  "quantity": 500.0,
  "shop_id": 1
}
```

### 8. Get Stock History
```bash
TOKEN="token_here"

curl -X GET "http://localhost:5000/api/stock/history?warehouse_id=1&limit=20" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "count": 3,
  "transactions": [
    {
      "id": 51,
      "warehouse_id": 1,
      "shop_id": 1,
      "quantity": 500.0,
      "type": "outbound",
      "timestamp": "2024-01-20T14:30:00",
      "notes": "Dispatch to shop"
    }
  ]
}
```

---

## 💳 BENEFICIARY TRANSACTION ENDPOINTS

### 9. Distribute Goods to Beneficiary (with Fraud Detection)
```bash
TOKEN="shop_manager_token"

curl -X POST http://localhost:5000/api/transactions/distribute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 5,
    "shop_id": 1,
    "quantity": 15.0
  }'

# Response (Normal):
{
  "message": "Distribution completed",
  "transaction_id": 100,
  "user_id": 5,
  "shop_id": 1,
  "quantity": 15.0,
  "fraud_risk": {
    "is_fraud": false,
    "risk_score": 0.22,
    "reason": "ML: Normal transaction | Rules: No rule violations",
    "confidence": "low"
  }
}

# Response (Fraudulent):
{
  "message": "Distribution completed",
  "transaction_id": 101,
  "user_id": 5,
  "shop_id": 1,
  "quantity": 180.0,
  "fraud_risk": {
    "is_fraud": true,
    "risk_score": 0.82,
    "reason": "ML: Anomaly detected (score: 0.92) | Rules: High quantity: 180.0 exceeds max 50.0",
    "confidence": "high"
  }
}
```

### 10. Get All Transactions
```bash
TOKEN="token_here"

curl -X GET "http://localhost:5000/api/transactions/all?shop_id=1&limit=50" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "count": 25,
  "transactions": [
    {
      "id": 100,
      "user_id": 5,
      "shop_id": 1,
      "quantity": 15.0,
      "timestamp": "2024-01-20T14:35:00"
    }
  ]
}
```

### 11. Get User Transaction History
```bash
TOKEN="token_here"
USER_ID=5

curl -X GET "http://localhost:5000/api/transactions/user/$USER_ID/history?limit=20" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "user_id": 5,
  "user_name": "Beneficiary 5",
  "count": 6,
  "total_quantity": 87.5,
  "avg_quantity": 14.58,
  "transactions": [
    {
      "id": 100,
      "shop_id": 1,
      "quantity": 15.0,
      "timestamp": "2024-01-20T14:35:00"
    }
  ]
}
```

---

## 🚨 FRAUD DETECTION ENDPOINTS

### 12. Get Fraud Alerts
```bash
TOKEN="admin_token"

# Get recent high-risk alerts
curl -X GET "http://localhost:5000/api/fraud/alerts?limit=20&risk_score_min=0.7&days=7" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "count": 3,
  "filters": {
    "limit": 20,
    "risk_score_min": 0.7,
    "days": 7,
    "is_anomaly": null
  },
  "alerts": [
    {
      "id": 1,
      "transaction_id": 101,
      "transaction_type": "beneficiary",
      "reason": "High quantity distribution detected",
      "risk_score": 0.85,
      "is_anomaly": true,
      "created_at": "2024-01-20T14:40:00"
    }
  ]
}
```

### 13. Get Fraud Alert Details
```bash
TOKEN="admin_token"
ALERT_ID=1

curl -X GET "http://localhost:5000/api/fraud/alerts/$ALERT_ID" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "alert": {
    "id": 1,
    "reason": "High quantity distribution detected",
    "risk_score": 0.85,
    "is_anomaly": true,
    "created_at": "2024-01-20T14:40:00"
  },
  "transaction": {
    "type": "beneficiary",
    "user_id": 5,
    "user_name": "Beneficiary 5",
    "shop_id": 1,
    "quantity": 180.0,
    "timestamp": "2024-01-20T14:40:00"
  }
}
```

### 14. Get Fraud Statistics
```bash
TOKEN="admin_token"

curl -X GET "http://localhost:5000/api/fraud/statistics?days=30" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "period_days": 30,
  "statistics": {
    "total_alerts": 15,
    "high_risk_alerts": 5,
    "anomalies_detected": 8,
    "average_risk_score": 0.58,
    "beneficiary_alerts": 12,
    "stock_alerts": 3
  }
}
```

---

## 📝 GRIEVANCE ENDPOINTS

### 15. Create Grievance
```bash
TOKEN="beneficiary_token"

curl -X POST http://localhost:5000/api/grievance \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 5,
    "description": "Did not receive the full quantity last time"
  }'

# Response:
{
  "message": "Grievance created successfully",
  "grievance_id": 10,
  "status": "open"
}
```

### 16. Get All Grievances
```bash
TOKEN="token_here"

# For beneficiaries: shows their own grievances
# For admins: shows all grievances

curl -X GET "http://localhost:5000/api/grievance/all?status=open&limit=50" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "count": 8,
  "grievances": [
    {
      "id": 10,
      "user_id": 5,
      "description": "Did not receive the full quantity last time",
      "status": "open",
      "created_at": "2024-01-20T15:00:00",
      "updated_at": "2024-01-20T15:00:00"
    }
  ]
}
```

### 17. Get Grievance Details
```bash
TOKEN="token_here"
GRIEVANCE_ID=10

curl -X GET "http://localhost:5000/api/grievance/$GRIEVANCE_ID" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "grievance": {
    "id": 10,
    "user_id": 5,
    "user_name": "Beneficiary 5",
    "description": "Did not receive the full quantity last time",
    "status": "open",
    "created_at": "2024-01-20T15:00:00",
    "updated_at": "2024-01-20T15:00:00"
  }
}
```

### 18. Update Grievance Status (Admin Only)
```bash
TOKEN="admin_token"
GRIEVANCE_ID=10

curl -X PUT "http://localhost:5000/api/grievance/$GRIEVANCE_ID/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved"
  }'

# Response:
{
  "message": "Grievance status updated",
  "grievance_id": 10,
  "status": "resolved"
}
```

### 19. Get Grievance Statistics (Admin Only)
```bash
TOKEN="admin_token"

curl -X GET "http://localhost:5000/api/grievance/statistics" \
  -H "Authorization: Bearer $TOKEN"

# Response:
{
  "statistics": {
    "total": 15,
    "open": 8,
    "resolved": 5,
    "closed": 2,
    "resolution_rate": 46.67
  }
}
```

---

## ⚠️ ERROR RESPONSES

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized"
}
```

### 403 Forbidden
```json
{
  "error": "Only admins can add warehouses"
}
```

### 404 Not Found
```json
{
  "error": "Warehouse not found"
}
```

### 409 Conflict
```json
{
  "error": "User with this ID already exists"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error message"
}
```

---

## 🧪 COMPLETE TEST WORKFLOW

### Step 1: Login as Admin
```bash
ADMIN_TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"unique_id":"ADMIN123456","password":"admin_pass"}' | \
  jq -r '.token')

echo "Admin Token: $ADMIN_TOKEN"
```

### Step 2: Add Stock to Warehouse
```bash
curl -X POST http://localhost:5000/api/stock/warehouse/1/add-stock \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5000, "notes": "Test supply"}'
```

### Step 3: Dispatch to Shop
```bash
curl -X POST http://localhost:5000/api/stock/warehouse/1/dispatch \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"shop_id": 1, "quantity": 1000}'
```

### Step 4: Login as Shop Manager
```bash
SHOP_TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"unique_id":"SHOP000000","password":"shop_pass"}' | \
  jq -r '.token')

echo "Shop Token: $SHOP_TOKEN"
```

### Step 5: Distribute to Beneficiary
```bash
curl -X POST http://localhost:5000/api/transactions/distribute \
  -H "Authorization: Bearer $SHOP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "shop_id": 1, "quantity": 15}'
```

### Step 6: Check Fraud Alerts (as Admin)
```bash
curl -X GET "http://localhost:5000/api/fraud/alerts?limit=10" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### Step 7: Login as Beneficiary
```bash
BENEFICIARY_TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"unique_id":"BENEFICIARY000000","password":"beneficiary_pass"}' | \
  jq -r '.token')
```

### Step 8: File Grievance
```bash
curl -X POST http://localhost:5000/api/grievance \
  -H "Authorization: Bearer $BENEFICIARY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "description": "Test grievance"}'
```

### Step 9: View Transaction History
```bash
curl -X GET "http://localhost:5000/api/transactions/user/2/history" \
  -H "Authorization: Bearer $BENEFICIARY_TOKEN"
```

---

## 📊 PERFORMANCE BENCHMARKS

### Expected Response Times
- Authentication: 80-150ms
- Simple queries: 20-50ms
- Complex queries: 100-200ms
- Fraud detection: 40-80ms
- Total distribution: 200-400ms

### Test Load
```bash
# Using Apache Bench for load testing
ab -n 1000 -c 10 http://localhost:5000/api/health

# Expected: ~1000 requests in 2-3 seconds
```

---

## 🔍 DEBUGGING TIPS

### Enable Request Logging
```bash
# Add to Flask app
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Database
```bash
# View all users
sqlite3 pds_platform.db "SELECT * FROM users;"

# View fraud alerts
sqlite3 pds_platform.db "SELECT * FROM fraud_alerts WHERE risk_score > 0.5;"
```

### Monitor ML Model
```bash
# Check model file
ls -lh backend/ml/models/fraud_detection_model.pkl

# Verify model works
python -c "import pickle; m = pickle.load(open('backend/ml/models/fraud_detection_model.pkl', 'rb')); print('Model loaded:', type(m))"
```

---

## ✅ VALIDATION CHECKLIST

- [ ] All endpoints accessible and returning data
- [ ] Authentication tokens valid and expiring correctly
- [ ] Fraud detection triggering on high-risk transactions
- [ ] Database transactions recording correctly
- [ ] Admin can manage warehouses and shops
- [ ] Shop managers can distribute goods
- [ ] Beneficiaries can view history and file grievances
- [ ] Role-based access control working
- [ ] Error responses formatted correctly
- [ ] Performance within acceptable range

---

**Ready for comprehensive API testing!**
