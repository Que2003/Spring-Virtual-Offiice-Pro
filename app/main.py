import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

app = FastAPI(title="Spring Virtual Office Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOT_INDEX = ROOT_DIR / "index.html"
STATIC_DIR = Path(__file__).resolve().parent / "static"

# MOBILE / CSS SUPPORT
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    message: str
    name: Optional[str] = None


SYSTEM_PROMPT = """
You are SpringBot, the AI assistant for Spring Virtual Office Pro.
You help users with office questions, scheduling guidance, support requests,
calming conversation, and clear next steps. Keep answers helpful, warm, and concise.
If someone sounds distressed or says they need emotional help, encourage them to reach
out to a trusted person or emergency services if they are in immediate danger, and say
that a human follow-up can be scheduled.
""".strip()


def fallback_reply(message: str) -> str:
    lower = message.lower()

    if any(word in lower for word in [
        "sad", "depressed", "anxious",
        "stressed", "overwhelmed",
        "lonely", "hurt"
    ]):
        return (
            "I hear you. I can help you slow down and explain what is going on. "
            "If this feels urgent or unsafe, please contact emergency services "
            "or someone you trust right now. "
            "For Spring Office, I can also help you request a follow-up conversation."
        )

    if any(word in lower for word in [
        "appointment", "schedule", "book", "meeting"
    ]):
        return (
            "I can help with scheduling. "
            "Tell me the best day, time, and what the appointment is for."
        )

    if any(word in lower for word in [
        "music", "song", "play"
    ]):
        return (
            "Music support is part of the SpringBot plan. "
            "Tell me the vibe you want, like calm, focus, or uplifting."
        )

    return (
        "SpringBot is connected. "
        "I can help with questions, scheduling, office support, and next steps."
    )


async def generate_reply(message: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return fallback_reply(message)

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                },
            ],
            temperature=0.6,
            max_tokens=220,
        )

        return (
            response.choices[0].message.content
            or fallback_reply(message)
        )

    except Exception:
        return fallback_reply(message)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Spring Virtual Office Pro"
    }


@app.get("/", response_class=HTMLResponse)
def home():
    if ROOT_INDEX.exists():
        return FileResponse(ROOT_INDEX)

    return HTMLResponse("""
    <h1>Spring Virtual Office Pro</h1>
    <p>SpringBot backend is online.</p>
    """)


@app.get("/chat", response_class=HTMLResponse)
def chat_page():

    chat_html = STATIC_DIR / "chat.html"

    if chat_html.exists():
        return FileResponse(chat_html)

    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">

    <head>
      <meta charset="UTF-8" />
      <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
      />

      <title>SpringBot Chat</title>

      <style>

        *{
          box-sizing:border-box;
        }

        body{
          margin:0;
          min-height:100vh;
          font-family:Segoe UI,Arial,sans-serif;
          color:#eef7ff;
          background:linear-gradient(135deg,#07111f,#0b2740);
          display:grid;
          place-items:center;
          padding:16px;
        }

        .card{
          width:min(760px,100%);
          background:rgba(255,255,255,.12);
          border:1px solid rgba(255,255,255,.22);
          border-radius:28px;
          padding:24px;
          box-shadow:0 30px 80px rgba(0,0,0,.35);
          backdrop-filter:blur(18px);
        }

        h1{
          font-size:clamp(2rem,5vw,4rem);
          margin:0 0 8px;
          letter-spacing:-.05em;
        }

        .muted{
          color:#aac3d9;
          line-height:1.6;
          margin-bottom:20px;
        }

        #log{
          display:grid;
          gap:12px;
          margin:18px 0;
          max-height:420px;
          overflow:auto;
        }

        .bubble{
          padding:13px 15px;
          border-radius:18px;
          background:rgba(255,255,255,.1);
          line-height:1.5;
          word-wrap:break-word;
        }

        .user{
          justify-self:end;
          background:rgba(102,217,255,.18);
        }

        .bot{
          justify-self:start;
          background:rgba(141,255,203,.14);
        }

        form{
          display:flex;
          gap:10px;
          background:rgba(0,0,0,.18);
          border:1px solid rgba(255,255,255,.18);
          border-radius:18px;
          padding:10px;
        }

        input{
          flex:1;
          background:transparent;
          border:0;
          outline:0;
          color:#fff;
          padding:12px;
          font-size:1rem;
        }

        button{
          border:0;
          border-radius:14px;
          padding:14px 18px;
          font-weight:800;
          background:linear-gradient(135deg,#66d9ff,#8dffcb);
          color:#03111c;
          cursor:pointer;
        }

        @media (max-width: 600px){

          .card{
            padding:18px;
            border-radius:20px;
          }

          form{
            flex-direction:column;
          }

          button{
            width:100%;
          }

        }

      </style>
    </head>

    <body>

      <main class="card">

        <h1>Spring Office</h1>

        <p class="muted">
          SpringBot is online.
          Ask a question, request support,
          or start a scheduling conversation.
        </p>

        <div id="log">
          <div class="bubble bot">
            Hey, I’m SpringBot. How can I help today?
          </div>
        </div>

        <form id="form">

          <input
            id="message"
            placeholder="Type your message..."
            autocomplete="off"
            aria-label="Message SpringBot"
          />

          <button>
            Send
          </button>

        </form>

      </main>

      <script>

        const form = document.getElementById('form');
        const input = document.getElementById('message');
        const log = document.getElementById('log');

        function add(text, cls){

          const b = document.createElement('div');

          b.className = 'bubble ' + cls;

          b.textContent = text;

          log.appendChild(b);

          log.scrollTop = log.scrollHeight;
        }

        form.addEventListener('submit', async e => {

          e.preventDefault();

          const message = input.value.trim();

          if(!message) return;

          add(message, 'user');

          input.value='';

          try{

            const res = await fetch('/api/chat', {
              method:'POST',
              headers:{
                'Content-Type':'application/json'
              },
              body:JSON.stringify({message})
            });

            const data = await res.json();

            add(
              data.reply ||
              'SpringBot is online, but I could not read that response.',
              'bot'
            );

          }catch(err){

            add(
              'Connection issue — please try again in a moment.',
              'bot'
            );

          }

        });

      </script>

    </body>
    </html>
    """)


@app.post("/api/chat")
async def api_chat(payload: ChatRequest):

    message = payload.message.strip()

    if not message:
        return JSONResponse({
            "reply": "Send me a message and I’ll help."
        })

    reply = await generate_reply(message)

    return {
        "reply": reply
    }


@app.post("/chat")
async def chat_alias(payload: ChatRequest):
    return await api_chat(payload)