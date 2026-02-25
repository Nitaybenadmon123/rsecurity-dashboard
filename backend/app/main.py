from fastapi import FastAPI, HTTPException, Query ,status, Depends, Header
from typing import Optional, List
import json
import os


from .db import init_db, get_conn
from .schemas import ReportCreate, ReportOut

app = FastAPI(title="RSecurity Reports API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "RSecurity Backend is running"}

@app.post("/report", response_model=ReportOut, status_code=201)
def create_report(report: ReportCreate):
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
def get_report(id: int):
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
def list_reports(tag: Optional[str] = Query(default=None)):
    conn = get_conn()
    try:
        rows = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
        reports: List[ReportOut] = []
        for row in rows:
            tags = json.loads(row["tags"])
            if tag and tag not in tags:
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

@app.delete("/report/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(id: int):
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM reports WHERE id = ?", (id,))
        conn.commit()

        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Report not found")

        return
    finally:
        conn.close()