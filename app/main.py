import os
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

try:
    from openai import OpenAI
except:
    OpenAI = None

app = FastAPI(title="Spring Virtual Office")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    name: Optional[str] = None


SYSTEM_PROMPT = """
You are SpringBot, the AI assistant for Spring Virtual Office.
You are futuristic, intelligent, professional, calm, and helpful.
Keep responses concise and useful.
""".strip()


def fallback_reply(message: str):

    lower = message.lower()

    if any(word in lower for word in [
        "sad", "depressed", "anxious",
        "hurt", "lonely", "stressed"
    ]):
        return (
            "I hear you. Take a breath and slow things down. "
            "I'm here with you."
        )

    if any(word in lower for word in [
        "appointment", "schedule", "meeting"
    ]):
        return (
            "I can help schedule that. "
            "Tell me the day and time."
        )

    return "SpringBot is online and ready to help."


async def generate_reply(message: str):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return fallback_reply(message)

    try:

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            max_tokens=200
        )

        return response.choices[0].message.content

    except:
        return fallback_reply(message)


@app.get("/")
async def home():

    return HTMLResponse("""

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
  name="viewport"
  content="width=device-width,
  initial-scale=1.0,
  viewport-fit=cover"
/>

<title>
Spring Virtual Office
</title>

<style>

*{
  box-sizing:border-box;
  -webkit-tap-highlight-color:transparent;
}

:root{

  --bg:
    linear-gradient(
      135deg,
      #050816,
      #0b1120,
      #020617
    );

  --panel:
    rgba(15,23,42,0.72);

  --text:#f8fafc;

  --muted:#94a3b8;

  --border:
    rgba(255,255,255,0.12);

  --accent:#4ade80;

  --accent2:#38bdf8;

}

body{

  margin:0;

  font-family:
    Arial,
    sans-serif;

  background:var(--bg);

  color:var(--text);

  height:100dvh;

  overflow:hidden;

  display:flex;

  flex-direction:column;

}

header{

  display:flex;

  justify-content:space-between;

  align-items:center;

  padding:16px;

  background:
    rgba(2,6,23,0.78);

  border-bottom:
    1px solid var(--border);

  backdrop-filter:blur(20px);

}

.brand{

  display:flex;

  align-items:center;

  gap:12px;

}

.logo{

  width:52px;

  height:52px;

  border-radius:16px;

  display:grid;

  place-items:center;

  background:
    linear-gradient(
      135deg,
      rgba(74,222,128,0.3),
      rgba(56,189,248,0.2)
    );

  font-size:28px;

}

.title{

  font-size:22px;

  font-weight:800;

}

.status{

  color:var(--accent);

  margin-top:3px;

  font-size:14px;

}

.right{

  display:flex;

  gap:10px;

  align-items:center;

}

select,
.clear{

  border:
    1px solid var(--border);

  background:
    rgba(255,255,255,0.06);

  color:var(--text);

  border-radius:999px;

  padding:10px 14px;

}

main{

  flex:1;

  overflow-y:auto;

  padding:20px;

  padding-bottom:220px;

  display:flex;

  flex-direction:column;

  gap:14px;

}

.welcome{

  margin-top:30px;

  background:var(--panel);

  border:
    1px solid var(--border);

  border-radius:30px;

  padding:40px 24px;

  text-align:center;

  backdrop-filter:blur(25px);

}

.welcome h1{

  margin:0;

  font-size:42px;

}

.welcome p{

  color:var(--muted);

  line-height:1.7;

  margin-top:16px;

}

.bubble{

  max-width:85%;

  padding:14px 16px;

  border-radius:22px;

  line-height:1.5;

  word-wrap:break-word;

}

.user{

  align-self:flex-end;

  background:
    linear-gradient(
      135deg,
      rgba(74,222,128,0.25),
      rgba(56,189,248,0.2)
    );

}

.bot{

  align-self:flex-start;

  background:var(--panel);

  border:
    1px solid var(--border);

}

form{

  position:fixed;

  left:0;

  right:0;

  bottom:120px;

  display:flex;

  gap:12px;

  padding:14px;

  background:
    rgba(2,6,23,0.82);

  border-top:
    1px solid var(--border);

  backdrop-filter:blur(25px);

}

input{

  flex:1;

  border:
    1px solid var(--border);

  border-radius:18px;

  padding:16px;

  font-size:16px;

  background:
    rgba(255,255,255,0.06);

  color:var(--text);

  outline:none;

}

button{

  border:0;

  border-radius:18px;

  padding:0 20px;

  background:
    linear-gradient(
      135deg,
      var(--accent),
      var(--accent2)
    );

  color:white;

  font-weight:800;

  font-size:16px;

}

@media (max-width:700px){

  form{
    bottom:140px;
  }

  .welcome h1{
    font-size:28px;
  }

  .right{
    flex-direction:column;
  }

}

body[data-theme="light"]{

  --bg:#f8faf7;
  --panel:#ffffff;
  --text:#1f2933;
  --muted:#6b7280;
  --border:#e5e7eb;
  --accent:#5f8f62;
  --accent2:#38bdf8;

}

body[data-theme="emerald"]{

  --bg:
    linear-gradient(
      135deg,
      #03120d,
      #071a14,
      #020617
    );

  --panel:
    rgba(6,78,59,0.28);

  --text:#ecfdf5;

  --muted:#a7f3d0;

  --border:
    rgba(74,222,128,0.18);

  --accent:#34d399;

  --accent2:#4ade80;

}

body[data-theme="cyber"]{

  --bg:
    linear-gradient(
      135deg,
      #020617,
      #081120,
      #071a2f
    );

  --panel:
    rgba(8,47,73,0.4);

  --text:#e0f2fe;

  --muted:#7dd3fc;

  --border:
    rgba(56,189,248,0.25);

  --accent:#38bdf8;

  --accent2:#22d3ee;

}

body[data-theme="luxury"]{

  --bg:
    linear-gradient(
      135deg,
      #050505,
      #111111,
      #050505
    );

  --panel:
    rgba(24,24,27,0.78);

  --text:#fafaf9;

  --muted:#a8a29e;

  --border:#292524;

  --accent:#d4af37;

  --accent2:#facc15;

}

</style>

</head>

<body data-theme="black-glass">

<header>

<div class="brand">

<div class="logo">
🌿
</div>

<div>

<div class="title">
Spring Virtual Office
</div>

<div class="status">
● AI Assistant · Online
</div>

</div>

</div>

<div class="right">

<select id="themeSelect">

<option value="black-glass">
Black Glass
</option>

<option value="light">
Light
</option>

<option value="emerald">
Emerald
</option>

<option value="cyber">
Cyber
</option>

<option value="luxury">
Luxury
</option>

</select>

<button
  class="clear"
  onclick="clearChat()"
>
Clear
</button>

</div>

</header>

<main id="log">

<div
  class="welcome"
  id="welcome"
>

<h1>
Welcome to Spring Virtual Office
</h1>

<p>
Your futuristic AI workspace is online.
Ask questions, request support,
book appointments,
or chat with SpringBot.
</p>

</div>

</main>

<form id="chatForm">

<input
  id="message"
  type="text"
  placeholder="Type your message..."
  autocomplete="off"
/>

<button type="submit">
Send
</button>

</form>

<script>

const form =
  document.getElementById("chatForm");

const input =
  document.getElementById("message");

const log =
  document.getElementById("log");

const themeSelect =
  document.getElementById("themeSelect");

const savedTheme =
  localStorage.getItem("springTheme")
  || "black-glass";

document.body.setAttribute(
  "data-theme",
  savedTheme
);

themeSelect.value =
  savedTheme;

themeSelect.addEventListener(
  "change",
  () => {

    const theme =
      themeSelect.value;

    document.body.setAttribute(
      "data-theme",
      theme
    );

    localStorage.setItem(
      "springTheme",
      theme
    );

  }
);

function addBubble(text,type){

  const welcome =
    document.getElementById("welcome");

  if(welcome){
    welcome.remove();
  }

  const bubble =
    document.createElement("div");

  bubble.className =
    "bubble " + type;

  bubble.textContent =
    text;

  log.appendChild(bubble);

  log.scrollTop =
    log.scrollHeight;

}

function clearChat(){

  log.innerHTML = `
    <div class="welcome" id="welcome">

      <h1>
        Welcome to Spring Virtual Office
      </h1>

      <p>
        History cleared.
        I'm ready to help.
      </p>

    </div>
  `;

}

form.addEventListener(
  "submit",
  async function(e){

    e.preventDefault();

    const message =
      input.value.trim();

    if(!message) return;

    addBubble(
      message,
      "user"
    );

    input.value = "";

    try{

      const response =
        await fetch(
          "/api/chat",
          {
            method:"POST",

            headers:{
              "Content-Type":
              "application/json"
            },

            body:JSON.stringify({
              message:message
            })
          }
        );

      const data =
        await response.json();

      addBubble(
        data.reply ||
        "SpringBot could not respond.",
        "bot"
      );

    }catch(error){

      addBubble(
        "Connection issue. Please try again.",
        "bot"
      );

    }

  }
);

</script>

</body>
</html>

    """)


@app.post("/api/chat")
async def api_chat(payload: ChatRequest):

    message = payload.message.strip()

    if not message:
        return {
            "reply": "Send me a message."
        }

    reply = await generate_reply(message)

    return {
        "reply": reply
    }


@app.get("/health")
async def health():

    return {
        "status": "online"
    }