"""
ARCHITECTURE AND CONFIGURATION GUIDE
PDS Platform - Intelligent Distribution System
"""

# ==============================================================================
# SYSTEM ARCHITECTURE OVERVIEW
# ==============================================================================

## Components

1. **Backend (Flask)**
   - REST API server
   - Database ORM (SQLAlchemy)
   - Authentication (JWT)
   - Business logic

2. **Machine Learning**
   - Isolation Forest model
   - Feature engineering
   - Fraud detection engine
   - Rule-based checks

3. **Frontend (Bootstrap)**
   - Admin dashboard
   - Shop panel
   - Beneficiary portal
   - Charts and visualizations

4. **Database (SQLite)**
   - 7 core models
   - Relational schema
   - Transaction logs
   - Alert records

# ==============================================================================
# DATABASE SCHEMA
# ==============================================================================

Model: User
├── id (PK)
├── name
├── unique_id (UNIQUE)
├── password (HASHED)
├── role (ENUM: admin, shop, beneficiary)
└── created_at

Model: Warehouse
├── id (PK)
├── name
├── location
└── created_at

Model: Shop
├── id (PK)
├── name
├── location
├── warehouse_id (FK)
├── current_stock
└── created_at

Model: StockTransaction
├── id (PK)
├── warehouse_id (FK)
├── shop_id (FK, nullable)
├── quantity
├── transaction_type (inbound/outbound)
├── timestamp
└── notes

Model: BeneficiaryTransaction
├── id (PK)
├── user_id (FK)
├── shop_id (FK)
├── quantity
└── timestamp

Model: Grievance
├── id (PK)
├── user_id (FK)
├── description
├── status (open/resolved/closed)
├── created_at
└── updated_at

Model: FraudAlert
├── id (PK)
├── stock_transaction_id (FK, nullable)
├── beneficiary_transaction_id (FK, nullable)
├── reason
├── risk_score (0-1)
├── is_anomaly (0/1)
└── created_at

# ==============================================================================
# FRAUD DETECTION LOGIC
# ==============================================================================

## Feature Engineering

Input Transaction → Extract Features
├── 1. Quantity: Amount of goods
├── 2. Frequency: Transactions per day
├── 3. Time Gap: Hours since last transaction
├── 4. Deviation: % deviation from average
├── 5. Hour: Time of day (0-23)
└── 6. Day of Week: Day pattern (0-6)

## ML Detection (Isolation Forest)

Features → Model Prediction
├── Anomaly Score (raw output)
├── Normalize to Risk Score (0-1)
├── Compare to Threshold (0.5)
└── Flag if anomaly (confidence-based)

## Rule-Based Detection

Transaction Data + History → Rule Checks
├── Rule 1: Duplicate usage within 5 minutes
├── Rule 2: High quantity (>50kg)
├── Rule 3: Multiple transactions today (>2)
└── Rule 4: Stock mismatch (request > available)

## Risk Score Calculation

final_risk = (ml_risk * 0.6) + (rule_risk * 0.4)

Decision:
- If final_risk > 0.5: Mark as fraud
- If is_anomaly = 1: Mark as fraud
- Create FraudAlert record
- Notify admin

# ==============================================================================
# API ARCHITECTURE
# ==============================================================================

## Request Flow

Client Request
    ↓
CORS Middleware
    ↓
JWT Authentication (except /auth/*)
    ↓
Route Handler
    ├─ Validate input
    ├─ Query database
    ├─ Apply business logic
    ├─ [Optional] Run fraud detection
    └─ Return response

## Authentication Flow

1. Register/Login
2. Receive JWT token (valid 24 hours)
3. Include in Authorization header: "Bearer <token>"
4. Validate on each request
5. If expired, get new token

## API Endpoints (20+)

Authentication (3):
├── POST /auth/register
├── POST /auth/login
└── POST /auth/verify-token

Stock Management (4):
├── GET /stock/warehouses
├── POST /stock/add-warehouse
├── POST /stock/warehouse/{id}/add-stock
├── POST /stock/warehouse/{id}/dispatch
└── GET /stock/history

Transactions (3):
├── POST /transactions/distribute
├── GET /transactions/all
└── GET /transactions/user/{id}/history

Fraud (3):
├── GET /fraud/alerts
├── GET /fraud/alerts/{id}
└── GET /fraud/statistics

Grievance (5):
├── POST /grievance
├── GET /grievance/all
├── GET /grievance/{id}
├── PUT /grievance/{id}/status
└── GET /grievance/statistics

Health:
└── GET /health

# ==============================================================================
# FRAUD DETECTION RULES
# ==============================================================================

Rule 1: Duplicate Usage
├── Time Window: 5 minutes
├── Trigger: Transaction within 5 min of last
├── Risk Score: +0.30
└── Action: Flag transaction

Rule 2: Abnormal High Distribution
├── Threshold: 50kg per transaction
├── Trigger: Quantity > 50kg
├── Risk Score: +0.25
└── Action: Flag transaction

Rule 3: Multiple Transactions
├── Daily Limit: 2 transactions/day
├── Trigger: >2 transactions today
├── Risk Score: +0.20
└── Action: Flag transaction

Rule 4: Stock Mismatch
├── Tolerance: 10%
├── Trigger: Request > Available (×1.1)
├── Risk Score: +0.25
└── Action: Flag transaction

ML Detection:
├── Algorithm: Isolation Forest
├── Training: 900 samples (800 normal, 100 anomaly)
├── Threshold: 0.5 risk score
└── Output: Anomaly flag + confidence

# ==============================================================================
# SECURITY MEASURES
# ==============================================================================

Authentication:
├── JWT tokens (24-hour expiration)
├── Password hashing (bcrypt)
├── Role-based access control
└── Token validation on each request

Authorization:
├── Admin: Full access
├── Shop: Can manage distribution
├── Beneficiary: Can view own data
└── Granular permission checks

Input Validation:
├── Required field checks
├── Type validation
├── Range validation
├── SQL injection prevention (ORM)
└── CORS policy enforcement

Data Protection:
├── Hashed passwords in DB
├── JWT tokens (no passwords)
├── No sensitive data in logs
├── Secure session cookies
└── Error messages sanitized

# ==============================================================================
# DEPLOYMENT CONFIGURATION
# ==============================================================================

Development (Current):
├── Database: SQLite (local file)
├── Server: Flask development server
├── Debug: Enabled
├── CORS: Enabled for localhost
└── Port: 5000

Production Ready:
├── Database: PostgreSQL/MySQL
├── Server: Gunicorn + Nginx
├── Debug: Disabled
├── CORS: Restricted origins
├── HTTPS: Required
├── Port: 443
└── Environment: .env file (not in repo)

Docker Support:
├── Dockerfile template available
├── docker-compose.yml for services
├── Multi-stage builds
└── Environment-based config

# ==============================================================================
# PERFORMANCE OPTIMIZATION
# ==============================================================================

Database:
├── Indexed queries
├── Connection pooling
├── Query caching
└── Transaction batching

API:
├── Response caching
├── Pagination support
├── Limit parameters
└── Efficient JSON serialization

ML Model:
├── Pre-trained (loaded once)
├── In-memory prediction
├── < 50ms per prediction
└── Batch prediction support

Frontend:
├── Bootstrap CDN (cached)
├── Chart.js library (async)
├── Minimal JavaScript
└── Responsive design

# ==============================================================================
# MONITORING & LOGGING
# ==============================================================================

Application Logs:
├── Error logs
├── Transaction logs
├── Authentication logs
├── Fraud alert logs
└── API request logs

Metrics to Monitor:
├── API response times
├── Database query times
├── Fraud detection accuracy
├── System uptime
├── Error rates
├── Active user count
└── Transaction throughput

Alerts:
├── High fraud rate detection
├── Database connection failures
├── API rate limit exceeded
├── Service downtime
└── ML model degradation

# ==============================================================================
# EXTENSION POINTS
# ==============================================================================

Adding New Features:

1. New API Endpoint:
   ├── Create route in src/routes/
   ├── Add authentication decorator
   ├── Implement business logic
   └── Add to routes/blueprint registry

2. New Fraud Rule:
   ├── Add to apply_rule_based_checks()
   ├── Define threshold/logic
   ├── Update documentation
   └── Test with sample data

3. New User Role:
   ├── Add to UserRole enum
   ├── Update permission checks
   ├── Create dashboard
   └── Add API access levels

4. New Dashboard:
   ├── Create HTML template
   ├── Add JavaScript/API calls
   ├── Style with Bootstrap
   └── Link from navigation

# ==============================================================================
# TESTING GUIDE
# ==============================================================================

Unit Testing:
├── Test models
├── Test authentication utils
├── Test fraud detection logic
└── Test API responses

Integration Testing:
├── Test API flows
├── Test database operations
├── Test authentication flow
└── Test fraud detection end-to-end

Load Testing:
├── 100+ concurrent users
├── 1000+ requests/minute
├── Database under load
└── ML model latency

# ==============================================================================
# TROUBLESHOOTING
# ==============================================================================

Common Issues:

Issue: Database locked
├── Cause: Multiple processes accessing DB
├── Solution: Delete .db file and restart
└── Prevention: Use PostgreSQL for production

Issue: Model not found
├── Cause: Training script not run
├── Solution: Run backend/ml/scripts/train_model.py
└── Prevention: Add pre-commit hook

Issue: JWT token expired
├── Cause: Token older than 24 hours
├── Solution: User must login again
└── Prevention: Auto-refresh before expiry

Issue: Port 5000 in use
├── Cause: Another service using port
├── Solution: Change port or kill process
└── Prevention: Use docker (isolated port)

# ==============================================================================
# FILE STRUCTURE
# ==============================================================================

pds-platform/
├── backend/
│   ├── app.py                    # Entry point
│   ├── src/
│   │   ├── config/app.py         # Flask factory
│   │   ├── database/db.py        # DB connection
│   │   ├── models/               # ORM models
│   │   ├── routes/               # API endpoints
│   │   ├── utils/                # Helpers
│   │   └── services/             # Business logic
│   └── ml/
│       ├── fraud_detector.py     # ML engine
│       ├── models/               # Saved models
│       └── scripts/              # Training
├── frontend/
│   ├── templates/                # HTML pages
│   └── static/                   # CSS/JS
├── data/                         # Data files
├── requirements.txt              # Dependencies
├── README.md                     # Full docs
├── QUICKSTART.md                # Quick guide
└── .env.example                 # Config template

# ==============================================================================
# VERSION HISTORY
# ==============================================================================

Version 1.0.0 (Current)
├── Core features implemented
├── 20+ API endpoints
├── Fraud detection active
├── Admin/Shop/Beneficiary roles
├── Dashboards created
└── Production-ready code

Future Enhancements:
├── WebSocket real-time updates
├── Mobile app (React Native)
├── Advanced analytics
├── Email/SMS notifications
├── Multi-language support
├── Blockchain audit trail
└── AI-powered recommendations

"""
