"""
Spring Virtual Office — FastAPI Backend
Routes: homepage, AI chat, appointments, admin panel
Railway-compatible version with proper path handling
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Optional
import sys

# Add the project root to Python path for Railway
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI

# ─── Config ────────────────────────────────────────────────────────────────────
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY", "")
OWNER_EMAIL      = os.getenv("OWNER_EMAIL", "")
BUSINESS_NAME    = os.getenv("BUSINESS_NAME", "Spring Virtual Office")
DB_PATH          = os.getenv("DB_PATH", "spring_office.db")

client_ai = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = f"""You are the AI assistant for {BUSINESS_NAME}, a professional virtual office platform.
You help users with general questions, appointment scheduling, and empathetic support.
When collecting appointment info, guide users step by step.
Be warm, concise, and professional. Never provide medical, legal, or financial advice.
If a user appears in distress, respond with empathy and suggest professional resources.
"""

CRISIS_KEYWORDS = ["suicide","kill myself","end my life","want to die","self harm","hurt myself"]

# ─── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title=f"{BUSINESS_NAME} API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static website files
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# ─── DB Helpers ────────────────────────────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, preferred_time TEXT, reason TEXT,
        status TEXT DEFAULT 'pending', created_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS web_conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT, role TEXT, content TEXT, created_at TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

# ─── Models ────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    session_id: str
    message: str

class AppointmentRequest(BaseModel):
    name: str
    email: str
    preferred_time: str
    reason: str

# ─── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def homepage():
    html_path = os.path.join(static_path, "index.html")
    if os.path.exists(html_path):
        with open(html_path) as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Spring Virtual Office</h1><p>Static files not found.</p>")

@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    html_path = os.path.join(static_path, "chat.html")
    if os.path.exists(html_path):
        with open(html_path) as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Chat page not found.</h1>")

@app.get("/appointments", response_class=HTMLResponse)
async def appointments_page():
    html_path = os.path.join(static_path, "appointments.html")
    if os.path.exists(html_path):
        with open(html_path) as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Appointments page not found.</h1>")

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    html_path = os.path.join(static_path, "admin.html")
    if os.path.exists(html_path):
        with open(html_path) as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Admin page not found.</h1>")

# ─── API Endpoints ─────────────────────────────────────────────────────────────
@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT role,content FROM web_conversations WHERE session_id=? ORDER BY id DESC LIMIT 10",
        (req.session_id,)
    )
    rows = list(reversed(c.fetchall()))
    conn.close()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for row in rows:
        messages.append({"role": row["role"], "content": row["content"]})
    messages.append({"role": "user", "content": req.message})

    is_crisis = any(kw in req.message.lower() for kw in CRISIS_KEYWORDS)
    if is_crisis:
        reply = ("💙 It sounds like you're going through something very difficult. "
                 "Please reach out to the 988 Suicide & Crisis Lifeline by calling or texting **988**. "
                 "Help is available 24/7. You are not alone.")
    else:
        try:
            response = await client_ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=300,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Save to DB
    now = datetime.utcnow().isoformat()
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO web_conversations (session_id,role,content,created_at) VALUES (?,?,?,?)",
              (req.session_id, "user", req.message, now))
    c.execute("INSERT INTO web_conversations (session_id,role,content,created_at) VALUES (?,?,?,?)",
              (req.session_id, "assistant", reply, now))
    conn.commit()
    conn.close()

    return {"reply": reply, "is_crisis": is_crisis}


@app.post("/api/appointments")
async def create_appointment(req: AppointmentRequest):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO appointments (name,email,preferred_time,reason,created_at) VALUES (?,?,?,?,?)",
        (req.name, req.email, req.preferred_time, req.reason, datetime.utcnow().isoformat())
    )
    conn.commit()
    appt_id = c.lastrowid
    conn.close()
    return {"success": True, "id": appt_id, "message": "Appointment request received!"}


@app.get("/api/appointments")
async def list_appointments(secret: str = ""):
    admin_secret = os.getenv("ADMIN_SECRET", "spring-admin-2025")
    if secret != admin_secret:
        raise HTTPException(status_code=403, detail="Unauthorized")
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM appointments ORDER BY id DESC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return {"appointments": rows}


@app.patch("/api/appointments/{appt_id}")
async def update_appointment_status(appt_id: int, body: dict, secret: str = ""):
    admin_secret = os.getenv("ADMIN_SECRET", "spring-admin-2025")
    if secret != admin_secret:
        raise HTTPException(status_code=403, detail="Unauthorized")
    status = body.get("status", "pending")
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE appointments SET status=? WHERE id=?", (status, appt_id))
    conn.commit()
    conn.close()
    return {"success": True}


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": BUSINESS_NAME, "time": datetime.utcnow().isoformat()}
