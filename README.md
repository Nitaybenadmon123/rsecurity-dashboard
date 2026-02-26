# RSecurity Internship Assignment

This repository contains my solution for the RSecurity Internship Assignment.  
The project is divided into three parts: Frontend, Backend, and Security/Analysis.

I completed all three parts and structured them as independent modules, with a future goal of integrating them into a single unified system.

---

## 📁 Project Structure

```
rsecurity-dashboard/
│
├── frontend/           # Part 1 – Interactive Dashboard (React)
├── backend/            # Part 2 – FastAPI Reports API (Dockerized)
├── analysis_part_3/    # Part 3 – Log Analysis & Anomaly Detection
└── README.md
```

---

# ▶ How to Run

## 1️⃣ Frontend (Interactive Dashboard)

```
cd frontend
npm install
npm start
```

Then open:
```
http://localhost:3000
```

The dashboard loads local JSON data and provides:
- Search
- Sortable table
- KPI cards
- Charts (Bar + Pie)
- Responsive layout

---

## 2️⃣ Backend (FastAPI + SQLite + Docker)

### Option A – Run with Docker (Recommended)

From the `backend` folder:

```
docker build -t security-backend .
docker run --rm -p 8000:8000 -e API_KEY=YOUR_KEY -v "${PWD}\reports.db:/app/reports.db" security-backend
```

Then open:
```
http://127.0.0.1:8000/docs
```

### Option B – Run locally (without Docker)

```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API includes:
- Create report
- Get report by ID
- List reports (with tag & search filters)
- Delete report
- API key protection

---

## 3️⃣ Security / Log Analysis

```
cd analysis_part_3
python analyze_logs.py
```

This generates:
- `anomaly_report.json`
- Visualization PNG files

Detection includes:
- Brute-force detection (time-window based)
- External IP grouping
- Geo-hop detection
- Statistical anomaly detection (3-sigma rule)
- Severity scoring + mitigation suggestions

---

# 🧠 Assumptions Made

- Logs are trusted as structurally valid CSV inputs.
- Private IP ranges are defined as RFC1918 ranges.
- Brute-force detection uses a fixed time window (5 minutes).
- Statistical anomaly detection is based on mean + 3σ threshold.
- API key authentication is sufficient for this assignment scope.
- SQLite is sufficient for demonstration purposes.

---

# 🚀 Extra Notes

- All three parts are intentionally modular.
- The architecture allows future integration into a single system:
  - Backend serving logs
  - Analysis running as a service
  - Frontend consuming real API data instead of static JSON
- Docker volume mapping ensures persistent database usage.
- The project emphasizes readability, separation of concerns, and security awareness.

---

# 📊 Completed Parts

✅ Frontend  
✅ Backend  
✅ Security / Analysis  

Completing all three parts to demonstrate full-stack + security capability.

---

# 🎯 What I Focused On

- Clean, readable, and structured code
- Defensive logic (API key auth, validation, structured responses)
- Meaningful anomaly detection logic
- Clear mitigation recommendations
- Visualization for both operational and analytical insights
- Scalability mindset (future system integration)

---

Thank you for reviewing my work.
Looking forward to your feedback.