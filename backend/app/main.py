import os
import json
from typing import Optional, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.security import APIKeyHeader
import hmac

from .db import init_db, get_conn
from .schemas import ReportCreate, ReportOut

# Load environment variables from backend/.env
load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("Missing API_KEY. Create backend/.env with API_KEY=...")

app = FastAPI(title="RSecurity Reports API")

# Swagger-friendly API key auth (shows "Authorize" button)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_api_key(x_api_key: str = Depends(api_key_header)):
    if not x_api_key or not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "RSecurity Backend is running"}

@app.post("/report", response_model=ReportOut, status_code=201)
def create_report(report: ReportCreate, _: None = Depends(require_api_key)):
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO reports (title, content, tags, date) VALUES (?, ?, ?, ?)",
            (report.title, report.content, json.dumps(report.tags), report.date),
        )
        conn.commit()
        report_id = cur.lastrowid
        return ReportOut(id=report_id, **report.model_dump())
    finally:
        conn.close()

@app.get("/report/{id}", response_model=ReportOut)
def get_report(id: int, _: None = Depends(require_api_key)):
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM reports WHERE id = ?", (id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Report not found")

        return ReportOut(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            tags=json.loads(row["tags"]),
            date=row["date"],
        )
    finally:
        conn.close()

@app.get("/reports", response_model=List[ReportOut])
def list_reports(
    tag: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None, description="Free-text search in title/content"),
    _: None = Depends(require_api_key),
):
    conn = get_conn()
    try:
        rows = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
        reports: List[ReportOut] = []

        for row in rows:
            tags = json.loads(row["tags"])

            if tag and tag not in tags:
                continue

            if q:
                haystack = f"{row['title']} {row['content']}".lower()
                if q.lower() not in haystack:
                         continue

            reports.append(
                ReportOut(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    tags=tags,
                    date=row["date"],
                )
            )

        return reports
    finally:
        conn.close()

@app.delete("/report/{id}", status_code=204)
def delete_report(id: int, _: None = Depends(require_api_key)):
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM reports WHERE id = ?", (id,))
        conn.commit()

        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Report not found")

        return
    finally:
        conn.close()