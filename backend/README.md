# RSecurity Reports API (Backend)

A RESTful API built with FastAPI for managing security reports.

This backend includes:
- Create report
- Get report by ID
- List reports
- Delete report
- Search reports by text
- Filter by tag
- API key authentication
- SQLite database
- Docker support

---

## 🛠 Tech Stack

- Python 3.12
- FastAPI
- SQLite
- Uvicorn
- Docker

---

## 📂 Project Structure

backend/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── schemas.py
│   └── __init__.py
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── .env (not committed)

---

# 🚀 Running Locally (Without Docker)

## 1. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Create .env file inside backend/

```
API_KEY=your_super_secret_key_here
```

Make sure `.env` is in `.gitignore`.

## 4. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 🔐 Authentication

All endpoints except `/` require API key.

Header format:

```
X-API-Key: your_super_secret_key_here
```

Swagger supports authentication via the **Authorize** button.

---

# 📌 API Endpoints

## GET /
Health check endpoint.

---

## POST /report
Create new report.

Example body:

```json
{
  "title": "Phishing Campaign",
  "content": "Multiple suspicious login attempts detected",
  "tags": ["phishing", "auth"],
  "date": "2025-09-06"
}
```

---

## GET /report/{id}
Retrieve report by ID.

---

## DELETE /report/{id}
Delete report by ID.

---

## GET /reports
List all reports.

Optional query parameters:

- `q` → search inside title and content
- `tag` → filter by tag

Examples:

```
/reports?q=phishing
/reports?tag=auth
/reports?q=login&tag=auth
```

If no results are found:

```
200 OK
[]
```

---

# 🐳 Docker Support

## 1. Build Docker image

From backend folder:

```bash
docker build -t rsecurity-backend .
```

## 2. Run container

```bash
docker run --rm -p 8000:8000 -e API_KEY="your_super_secret_key_here" rsecurity-backend
```

Open Swagger:

```
http://127.0.0.1:8000/docs
```

---

# 🧠 Design Decisions

- API key stored as environment variable (not hardcoded)
- Secrets not committed to Git
- SQLite chosen for simplicity
- Dockerized for portability
- Clean separation between configuration and code

---

# ✅ Bonus Features Implemented

✔ API key authentication  
✔ Free-text search (`q`)  
✔ Tag filtering  
✔ DELETE endpoint  
✔ Dockerized application  

---

# 📬 Testing with curl

Example:

```bash
curl http://127.0.0.1:8000/reports \
  -H "X-API-Key: your_super_secret_key_here"
```

---

# 📎 Notes

- Database file is created automatically on first run.
- When running via Docker, the database exists inside the container.
- API key is required for secured endpoints.