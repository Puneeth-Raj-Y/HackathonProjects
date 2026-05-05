# GETTING STARTED - PDS PLATFORM

## 🎯 You Have Everything You Need!

The complete PDS Platform has been built and is ready to run.

---

## ⚡ RUN IN 10 MINUTES

### Open PowerShell & Navigate to Project
```powershell
cd c:\Users\punee\Desktop\VS\Hackathon\pds-platform
```

### Create & Activate Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Train ML Model
```powershell
cd backend/ml/scripts
python train_model.py
```
✓ Creates fraud detection model

### Generate Sample Data
```powershell
python generate_sample_data.py
```
✓ Creates database with test data

### Start Server
```powershell
cd ../../
python app.py
```

### ✅ Done! Server Running
```
http://localhost:5000/api
```

---

## 🧪 Quick Test

### In a New PowerShell Window:
```powershell
# Test API health
curl http://localhost:5000/api/health
```

### Expected Response:
```json
{"status":"ok","message":"PDS Platform API is running"}
```

---

## 🔐 Demo Credentials

**Admin**
- ID: `ADMIN123456`
- Password: `admin_pass`

**Shop Manager**
- ID: `SHOP000000`
- Password: `shop_pass`

**Beneficiary**
- ID: `BENEFICIARY000000`
- Password: `beneficiary_pass`

---

## 📚 Documentation Files

Read these in order:

1. **QUICKSTART.md** - 5-minute setup
2. **DEPLOYMENT_GUIDE.md** - Detailed setup
3. **API_TESTING_GUIDE.md** - Test all APIs
4. **ARCHITECTURE.md** - How it works
5. **README.md** - Complete documentation
6. **PROJECT_SUMMARY.md** - What was built

---

## 🎯 What You Have

✅ **Complete Backend** - 20+ REST APIs
✅ **ML Fraud Detection** - Real Isolation Forest
✅ **Database** - 7 models, relational schema
✅ **Frontend** - 3 dashboards
✅ **Sample Data** - Ready to test
✅ **Documentation** - 5 guides

---

## 🚀 Next Steps

1. Start the server (follow RUN IN 10 MINUTES above)
2. Test health endpoint
3. Review API_TESTING_GUIDE.md
4. Login with demo credentials
5. Explore dashboards
6. Test fraud detection
7. Review documentation

---

## ⚠️ Common Issues & Solutions

### "ModuleNotFoundError"
```powershell
pip install -r requirements.txt
```

### "Port 5000 already in use"
```powershell
# Kill the process or change port in backend/app.py
```

### "Model not found"
```powershell
cd backend/ml/scripts
python train_model.py
```

### "No data in database"
```powershell
cd backend/ml/scripts
python generate_sample_data.py
```

---

## 📊 Project Stats

- **Files**: 40+
- **Code**: 3,500+ lines
- **Endpoints**: 20+
- **Models**: 7
- **Features**: 30+
- **Documentation**: 5 guides

---

## 💡 Pro Tips

1. Keep server running in one window
2. Use another window for testing
3. Check logs in server window
4. Review documentation while testing
5. Modify fraud thresholds in fraud_detector.py
6. Add more sample data if needed

---

## 🎓 Learning Path

**Day 1: Setup & Testing**
- [ ] Complete setup
- [ ] Test all endpoints
- [ ] Review documentation

**Day 2: Understanding System**
- [ ] Study database schema
- [ ] Review API code
- [ ] Understand fraud detection

**Day 3: Customization**
- [ ] Modify fraud rules
- [ ] Add sample data
- [ ] Extend API endpoints

**Day 4: Production**
- [ ] Configure for production
- [ ] Set up monitoring
- [ ] Deploy to server

---

## 🆘 Need Help?

1. **Setup Issues**: See DEPLOYMENT_GUIDE.md
2. **API Issues**: See API_TESTING_GUIDE.md
3. **Understanding System**: See ARCHITECTURE.md
4. **Features**: See README.md
5. **What's Built**: See PROJECT_SUMMARY.md

---

## ✨ Highlights

- ✅ End-to-end working prototype
- ✅ Real ML fraud detection
- ✅ Production-quality code
- ✅ Comprehensive documentation
- ✅ Ready to extend
- ✅ Ready to deploy
- ✅ Ready to learn from

---

## 🎉 YOU'RE ALL SET!

**Start the server and begin exploring!**

```
Happy Coding! 🚀
```

---

For detailed information, see the documentation files included in the project directory.
