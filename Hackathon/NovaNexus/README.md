# 🌌 Nova Nexus: AI Precision Manufacturing

Nova Nexus is a next-generation Manufacturing Order Management System (MOMS) that leverages natural language processing to streamline factory workflows. Users interact with the system entirely through a conversational AI interface.

## 🚀 Features
- **Natural Language Order Creation**: "I need 200 titanium flanges by July 20"
- **Intelligent Status Updates**: "Mark order #3 as accepted"
- **Integrated Quality Logs**: "Quality update on order #3: passed inspection"
- **Futuristic Dashboard**: Real-time tracking with glassmorphic UI and neon accents.
- **Precision Extraction**: Automated extraction of quantity, material, part name, and deadlines.

## 🛠 Tech Stack
- **Frontend**: React, Vite, TailwindCSS, Framer Motion, Axios, Lucide React.
- **Backend**: FastAPI (Python), SQLAlchemy, SQLite.
- **AI/NLP**: spaCy (Entity Extraction), Regex-based intent classification.

---

## 📦 Setup Instructions

### 1. Backend Setup (FastAPI)
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
4. Start the server:
   ```bash
   python main.py
   ```
   *Backend will be running at http://localhost:8000*

### 2. Frontend Setup (React)
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   *Frontend will be running at http://localhost:5173*

---

## 🧪 Example Commands to Try
- *"Create an order for 500 aluminum brackets for August 15"*
- *"I need 100 brass couplings delivered next week"*
- *"Show all received orders"*
- *"Mark order #1 as in review"*
- *"Quality log for order #1: dimensions within tolerance (+/- 0.01mm)"*

---

## 📁 Architecture
```text
NovaNexus/
├── backend/
│   ├── database/    # DB Connection
│   ├── models/      # SQLAlchemy & Pydantic Models
│   ├── routes/      # API Endpoints (Chat, Orders)
│   ├── nlp/         # AI Extraction Engine
│   └── main.py      # Entry Point
└── frontend/
    ├── src/
    │   ├── components/ # Glassmorphic UI Components
    │   ├── services/   # API Integration
    │   └── App.jsx     # Main Layout
    └── tailwind.config.js
```

**Built for the "Nova Nexus" Hackathon Challenge.**
