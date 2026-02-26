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

## 🐳 Running the Backend with Docker (Important: SQLite Volume)

This backend uses **SQLite (`reports.db`)** for data persistence.

When running the app inside Docker, the database inside the container is **not the same** as the one on your local machine unless you explicitly mount it as a volume.

If you do not mount the database file, Docker will create a new empty database inside the container, and previously created records will not appear.

---

### 🔧 Build the Docker Image

From the `backend/` directory:

```bash
docker build -t security-backend .
```

---

### ▶️ Run with Database Volume (Recommended)

```bash
docker run --rm -p 8000:8000 \
  -e API_KEY="your_api_key_here" \
  -v ${PWD}/reports.db:/app/reports.db \
  security-backend
```

On Windows (PowerShell):

```powershell
docker run --rm -p 8000:8000 `
  -e API_KEY="your_api_key_here" `
  -v ${PWD}\reports.db:/app/reports.db `
  security-backend
```

This ensures that:
- The container uses the same `reports.db` file as your local project.
- Data persists between container runs.
- Existing records are accessible via the API.

---

### 🚫 What Happens Without a Volume?

If you run:

```bash
docker run --rm -p 8000:8000 -e API_KEY="..."
```

Docker will create a new empty `/app/reports.db` file inside the container.

As a result:
- `GET /report/{id}` may return `404`
- `GET /reports` may return an empty list
- Previously created records will not be visible

---

### 📌 API Authentication

All endpoints require the `X-API-Key` header:

```
X-API-Key: your_api_key_here
```

You can test endpoints via:

- Swagger UI → `http://localhost:8000/docs`
- cURL
- Postman
- Frontend integration

---

### 🧠 Why This Matters

In containerized environments, file paths are isolated from the host system.  
Mounting the database as a volume ensures proper data persistence and prevents confusion during development.


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
