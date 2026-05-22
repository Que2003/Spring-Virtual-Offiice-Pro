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

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Spring Virtual Office")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELS
# =========================

class ChatRequest(BaseModel):
    message: str
    name: Optional[str] = None


# =========================
# SUPERBOT SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are SpringBot.

You are highly intelligent, emotionally aware,
extremely human-like, witty, supportive,
creative, futuristic, strategic, and warm.

You behave like a best friend mixed with
an elite AI assistant.

You help with:
- emotional support
- life advice
- business
- AI
- coding
- scheduling
- creativity
- gaming
- productivity
- social advice
- tech support
- brainstorming
- decision making
- deep conversations

You NEVER sound robotic.

You speak naturally.

You have personality.

You are emotionally intelligent.

You ask follow-up questions naturally.

You are futuristic and cool.

You are part of Spring Virtual Office.
""".strip()


# =========================
# FALLBACK REPLIES
# =========================

def fallback_reply(message: str):

    lower = message.lower()

    if any(word in lower for word in [
        "sad",
        "depressed",
        "lonely",
        "hurt",
        "anxious",
        "stressed"
    ]):
        return (
            "I’m here with you. "
            "Talk to me. "
            "What’s been weighing on you lately?"
        )

    if any(word in lower for word in [
        "hello",
        "hi",
        "hey"
    ]):
        return (
            "Hey 👋 "
            "Good to see you. "
            "What’s going on?"
        )

    if any(word in lower for word in [
        "appointment",
        "schedule",
        "meeting"
    ]):
        return (
            "Absolutely. "
            "Tell me what you want to schedule."
        )

    return (
        "That’s interesting. "
        "Tell me more."
    )


# =========================
# OPENAI REPLY
# =========================

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

            temperature=0.9,
            max_tokens=400
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        print("OPENAI ERROR:", str(e))

        return fallback_reply(message)
        # =========================
# HOME PAGE
# =========================

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
  margin:0;
  padding:0;
  box-sizing:border-box;
  -webkit-tap-highlight-color:transparent;
}

:root{

  --bg:#050816;

  --panel:
    rgba(255,255,255,0.08);

  --text:#ffffff;

  --muted:#a1a1aa;

  --accent:#8b5cf6;

  --accent2:#06b6d4;

  --glass:
    blur(24px);

}

body{

  font-family:
    Arial,
    sans-serif;

  background:var(--bg);

  color:var(--text);

  overflow:hidden;

  height:100dvh;

  transition:
    background .4s ease,
    color .4s ease;

}

/* =====================
ANIMATED BACKGROUND
===================== */

.bg{

  position:fixed;

  inset:0;

  overflow:hidden;

  z-index:-2;

  background:
    radial-gradient(
      circle at top left,
      rgba(139,92,246,0.25),
      transparent 40%
    ),

    radial-gradient(
      circle at bottom right,
      rgba(6,182,212,0.18),
      transparent 40%
    ),

    #050816;

}

.orb{

  position:absolute;

  border-radius:50%;

  filter:blur(90px);

  animation:
    float 10s infinite ease-in-out;

}

.orb1{

  width:300px;
  height:300px;

  background:#8b5cf6;

  top:-80px;
  left:-80px;

}

.orb2{

  width:260px;
  height:260px;

  background:#06b6d4;

  bottom:-80px;
  right:-80px;

  animation-delay:2s;

}

@keyframes float{

  0%,100%{
    transform:
      translateY(0px)
      translateX(0px);
  }

  50%{
    transform:
      translateY(-30px)
      translateX(20px);
  }

}

/* =====================
HEADER
===================== */

header{

  position:fixed;

  top:0;
  left:0;
  right:0;

  height:80px;

  display:flex;

  justify-content:space-between;

  align-items:center;

  padding:0 28px;

  background:
    rgba(0,0,0,0.25);

  backdrop-filter:
    blur(24px);

  border-bottom:
    1px solid rgba(255,255,255,0.08);

  z-index:1000;

}

.brand{

  display:flex;

  align-items:center;

  gap:14px;

}

.logo{

  width:54px;
  height:54px;

  border-radius:18px;

  display:grid;

  place-items:center;

  font-size:28px;

  background:
    linear-gradient(
      135deg,
      rgba(139,92,246,0.6),
      rgba(6,182,212,0.5)
    );

  backdrop-filter:
    blur(20px);

  animation:
    pulse 4s infinite ease-in-out;

}

@keyframes pulse{

  0%,100%{
    transform:scale(1);
  }

  50%{
    transform:scale(1.08);
  }

}

.brand-text h2{

  font-size:20px;

}

.brand-text p{

  color:var(--muted);

  font-size:13px;

  margin-top:2px;

}

/* =====================
THEMES
===================== */

.theme-wrap{

  position:relative;

}

.theme-btn{

  border:none;

  padding:12px 18px;

  border-radius:14px;

  background:
    rgba(255,255,255,0.08);

  color:white;

  cursor:pointer;

  backdrop-filter:
    blur(20px);

}

.theme-menu{

  position:absolute;

  right:0;

  top:60px;

  width:220px;

  background:
    rgba(10,10,15,0.92);

  border:
    1px solid rgba(255,255,255,0.08);

  border-radius:18px;

  overflow:hidden;

  display:none;

  backdrop-filter:
    blur(30px);

}

.theme-menu.active{

  display:block;

}

.theme-option{

  padding:14px 18px;

  cursor:pointer;

  transition:.2s;

}

.theme-option:hover{

  background:
    rgba(255,255,255,0.08);

}

/* =====================
MAIN
===================== */

main{

  height:100dvh;

  display:flex;

  justify-content:center;

  align-items:center;

  text-align:center;

  padding:120px 24px 24px;

}

.hero{

  max-width:900px;

  animation:
    fadeUp 1s ease;

}

@keyframes fadeUp{

  from{
    opacity:0;
    transform:
      translateY(40px);
  }

  to{
    opacity:1;
    transform:
      translateY(0);
  }

}

.tag{

  color:#8b5cf6;

  letter-spacing:2px;

  font-size:12px;

  margin-bottom:24px;

}

.hero h1{

  font-size:72px;

  line-height:1.05;

  margin-bottom:24px;

}

.hero h1 span{

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #06b6d4
    );

  -webkit-background-clip:text;

  -webkit-text-fill-color:transparent;

}

.hero p{

  color:var(--muted);

  font-size:18px;

  line-height:1.8;

  max-width:700px;

  margin:auto;

}

.cta{

  margin-top:40px;

  display:flex;

  justify-content:center;

  gap:18px;

  flex-wrap:wrap;

}

.btn{

  padding:16px 28px;

  border-radius:18px;

  text-decoration:none;

  font-weight:700;

  transition:.25s;

}

.btn-primary{

  background:
    linear-gradient(
      135deg,
      #8b5cf6,
      #06b6d4
    );

  color:white;

}

.btn-primary:hover{

  transform:
    translateY(-4px);

}

.btn-secondary{

  background:
    rgba(255,255,255,0.08);

  color:white;

  backdrop-filter:
    blur(20px);

}

/* =====================
SIDEKICK
===================== */

.sidekick{

  position:fixed;

  right:30px;

  bottom:30px;

  z-index:500;

  cursor:pointer;

}

.avatar{

  width:90px;
  height:90px;

  border-radius:28px;

  background:
    linear-gradient(
      135deg,
      rgba(139,92,246,0.6),
      rgba(6,182,212,0.5)
    );

  display:flex;

  align-items:center;

  justify-content:center;

  font-size:42px;

  backdrop-filter:
    blur(20px);

  box-shadow:
    0 20px 50px rgba(0,0,0,0.4);

  animation:
    bounce 3s infinite ease-in-out;

}

@keyframes bounce{

  0%,100%{
    transform:
      translateY(0);
  }

  50%{
    transform:
      translateY(-12px);
  }

}

.sidekick-msg{

  position:absolute;

  bottom:110px;

  right:0;

  width:220px;

  padding:14px;

  border-radius:18px;

  background:
    rgba(255,255,255,0.08);

  backdrop-filter:
    blur(20px);

  font-size:14px;

  line-height:1.5;

  animation:
    fadeUp 1s ease;

}

/* =====================
MOBILE
===================== */

@media(max-width:768px){

  .hero h1{
    font-size:44px;
  }

  .hero p{
    font-size:15px;
  }

  .sidekick{
    right:18px;
    bottom:18px;
  }

  .avatar{
    width:74px;
    height:74px;
    font-size:34px;
  }

}

</style>

</head>

<body>

<div class="bg">

<div class="orb orb1"></div>

<div class="orb orb2"></div>

</div>

<header>

<div class="brand">

<div class="logo">
🌿
</div>

<div class="brand-text">

<h2>
Spring Virtual Office
</h2>

<p>
AI Powered Workspace
</p>

</div>

</div>

<div class="theme-wrap">

<button
  class="theme-btn"
  onclick="toggleThemes()"
>
🎨 Themes
</button>

<div
  class="theme-menu"
  id="themeMenu"
>

<div
  class="theme-option"
  onclick="setTheme('default')"
>
🌌 Futuristic
</div>

<div
  class="theme-option"
  onclick="setTheme('light')"
>
☀️ Light
</div>

<div
  class="theme-option"
  onclick="setTheme('holiday')"
>
🎄 Holiday
</div>

<div
  class="theme-option"
  onclick="setTheme('ocean')"
>
🌊 Ocean
</div>

<div
  class="theme-option"
  onclick="setTheme('matrix')"
>
🟢 Matrix
</div>

</div>

</div>

</header>

<main>

<div class="hero">

<div class="tag">
SPRING AI SYSTEM
</div>

<h1>

Your AI
<span>
Virtual Office
</span>

</h1>

<p>

SpringBot combines emotional intelligence,
AI reasoning,
virtual assistance,
deep conversation,
business tools,
and futuristic interaction
into one intelligent platform.

</p>

<div class="cta">

<a
  href="/chat"
  class="btn btn-primary"
>
Open SpringBot →
</a>

<a
  href="/discord"
  class="btn btn-secondary"
>
Discord Bot
</a>

</div>

</div>

</main>

<div
  class="sidekick"
  onclick="window.location.href='/chat'"
>

<div class="sidekick-msg">

Hey 👋<br>
Need help?<br>
Open SpringBot.

</div>

<div class="avatar">
🌿
</div>

</div>

<script>

function toggleThemes(){

  document
    .getElementById(
      "themeMenu"
    )
    .classList
    .toggle("active");

}

function setTheme(theme){

  localStorage.setItem(
    "spring-theme",
    theme
  );

  applyTheme(theme);

}

function applyTheme(theme){

  if(theme === "light"){

    document.body.style.background =
      "#f4f4f5";

  }

  else if(theme === "holiday"){

    document.body.style.background =
      "#3b0a0a";

  }

  else if(theme === "ocean"){

    document.body.style.background =
      "#031926";

  }

  else if(theme === "matrix"){

    document.body.style.background =
      "#020805";

  }

  else{

    document.body.style.background =
      "#050816";

  }

}

window.onload = () => {

  const saved =
    localStorage.getItem(
      "spring-theme"
    );

  if(saved){

    applyTheme(saved);

  }

}

</script>

</body>
</html>

    """)
    # =========================
# CHAT PAGE
# =========================

@app.get("/chat")
async def chat_page():

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
SpringBot Chat
</title>

<style>

*{
  margin:0;
  padding:0;
  box-sizing:border-box;
  -webkit-tap-highlight-color:transparent;
}

:root{
  --bg:#050816;
  --panel:rgba(255,255,255,0.08);
  --text:#ffffff;
  --muted:#a1a1aa;
  --accent:#8b5cf6;
  --accent2:#06b6d4;
  --border:rgba(255,255,255,0.12);
}

html,
body{
  width:100%;
  height:100%;
  overflow:hidden;
}

body{
  font-family:Arial,sans-serif;
  background:
    radial-gradient(circle at top left,rgba(139,92,246,0.22),transparent 35%),
    radial-gradient(circle at bottom right,rgba(6,182,212,0.18),transparent 35%),
    var(--bg);
  color:var(--text);
}

header{
  position:fixed;
  top:0;
  left:0;
  right:0;
  height:78px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 18px;
  background:rgba(0,0,0,0.35);
  backdrop-filter:blur(24px);
  border-bottom:1px solid var(--border);
  z-index:1000;
}

.brand{
  display:flex;
  align-items:center;
  gap:12px;
}

.avatar{
  width:50px;
  height:50px;
  border-radius:18px;
  display:grid;
  place-items:center;
  font-size:28px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  animation:botFloat 3s ease-in-out infinite;
}

@keyframes botFloat{
  0%,100%{transform:translateY(0)}
  50%{transform:translateY(-5px)}
}

.title{
  font-size:20px;
  font-weight:800;
}

.status{
  font-size:13px;
  color:var(--accent2);
  margin-top:2px;
}

.actions{
  display:flex;
  gap:8px;
  align-items:center;
}

.theme-select,
.clear{
  border:1px solid var(--border);
  background:rgba(255,255,255,0.08);
  color:white;
  border-radius:999px;
  padding:9px 12px;
  font-size:12px;
}

main{
  position:fixed;
  top:78px;
  left:0;
  right:0;
  bottom:135px;
  overflow-y:auto;
  padding:18px;
  display:flex;
  flex-direction:column;
  gap:14px;
}

.welcome{
  margin-top:35px;
  padding:32px 22px;
  text-align:center;
  border:1px solid var(--border);
  background:var(--panel);
  backdrop-filter:blur(24px);
  border-radius:28px;
  animation:fadeUp .7s ease;
}

@keyframes fadeUp{
  from{opacity:0;transform:translateY(20px)}
  to{opacity:1;transform:translateY(0)}
}

.welcome h1{
  font-size:34px;
  margin-bottom:14px;
}

.welcome p{
  color:var(--muted);
  line-height:1.7;
}

.bubble{
  max-width:86%;
  padding:14px 16px;
  border-radius:22px;
  line-height:1.5;
  word-wrap:break-word;
  animation:fadeUp .25s ease;
}

.user{
  align-self:flex-end;
  background:linear-gradient(135deg,rgba(139,92,246,0.45),rgba(6,182,212,0.35));
}

.bot{
  align-self:flex-start;
  background:var(--panel);
  border:1px solid var(--border);
  backdrop-filter:blur(20px);
}

.typing{
  display:none;
  align-self:flex-start;
  background:var(--panel);
  border:1px solid var(--border);
  border-radius:22px;
  padding:14px 18px;
  color:var(--muted);
}

.typing.show{
  display:block;
}

form{
  position:fixed;
  left:0;
  right:0;
  bottom:80px;
  display:flex;
  gap:10px;
  padding:12px;
  background:rgba(0,0,0,0.38);
  backdrop-filter:blur(28px);
  border-top:1px solid var(--border);
  z-index:1000;
}

input{
  flex:1;
  min-width:0;
  border:1px solid var(--border);
  background:rgba(255,255,255,0.08);
  color:white;
  border-radius:18px;
  padding:16px;
  font-size:16px;
  outline:none;
}

input::placeholder{
  color:var(--muted);
}

button{
  border:0;
  border-radius:18px;
  padding:0 18px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:white;
  font-weight:800;
  font-size:16px;
}

.sidekick{
  position:fixed;
  right:16px;
  bottom:160px;
  width:72px;
  height:72px;
  border-radius:24px;
  display:grid;
  place-items:center;
  font-size:34px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  box-shadow:0 20px 50px rgba(0,0,0,.45);
  animation:botFloat 3s ease-in-out infinite;
  z-index:900;
}

.hint{
  position:fixed;
  right:16px;
  bottom:240px;
  max-width:210px;
  padding:12px;
  border-radius:16px;
  background:var(--panel);
  border:1px solid var(--border);
  backdrop-filter:blur(20px);
  font-size:13px;
  color:var(--text);
  z-index:900;
}

body[data-theme="light"]{
  --bg:#f5f5f7;
  --panel:rgba(255,255,255,.75);
  --text:#111827;
  --muted:#6b7280;
  --accent:#5f8f62;
  --accent2:#38bdf8;
  --border:rgba(0,0,0,.12);
}

body[data-theme="holiday"]{
  --bg:#160707;
  --panel:rgba(80,10,10,.55);
  --text:#fff7ed;
  --muted:#fecaca;
  --accent:#dc2626;
  --accent2:#22c55e;
  --border:rgba(255,255,255,.16);
}

body[data-theme="ocean"]{
  --bg:#031926;
  --panel:rgba(14,116,144,.25);
  --text:#ecfeff;
  --muted:#a5f3fc;
  --accent:#06b6d4;
  --accent2:#14b8a6;
  --border:rgba(255,255,255,.14);
}

body[data-theme="matrix"]{
  --bg:#020805;
  --panel:rgba(0,80,40,.25);
  --text:#dcfce7;
  --muted:#86efac;
  --accent:#22c55e;
  --accent2:#16a34a;
  --border:rgba(34,197,94,.25);
}

@media(max-width:700px){
  header{
    height:76px;
    padding:0 12px;
  }

  .title{
    font-size:16px;
  }

  .actions{
    flex-direction:column;
  }

  main{
    top:76px;
    bottom:150px;
  }

  form{
    bottom:95px;
  }

  .sidekick{
    width:60px;
    height:60px;
    font-size:28px;
    bottom:170px;
  }

  .hint{
    display:none;
  }
}

</style>

</head>

<body>

<header>

<div class="brand">

<div class="avatar">
🌿
</div>

<div>
<div class="title">
SpringBot
</div>
<div class="status">
● SuperBot Online
</div>
</div>

</div>

<div class="actions">

<select
  class="theme-select"
  id="themeSelect"
>
<option value="default">Futuristic</option>
<option value="light">Light</option>
<option value="holiday">Holiday</option>
<option value="ocean">Ocean</option>
<option value="matrix">Matrix</option>
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
Hey, I’m SpringBot 🌿
</h1>

<p>
I’m your AI sidekick. Ask me about anything:
life, business, tech, scheduling, ideas,
Discord, or whatever is on your mind.
</p>

</div>

<div
  class="typing"
  id="typing"
>
SpringBot is thinking...
</div>

</main>

<div class="hint">
I’m your sidekick. I can guide users, answer questions, and help them find what they need.
</div>

<div
  class="sidekick"
  onclick="addBubble('You tapped SpringBot 🌿', 'bot')"
>
🌿
</div>

<form id="chatForm">

<input
  id="message"
  type="text"
  placeholder="Talk to SpringBot..."
  autocomplete="off"
/>

<button type="submit">
Send
</button>

</form>

<script>

const form = document.getElementById("chatForm");
const input = document.getElementById("message");
const log = document.getElementById("log");
const typing = document.getElementById("typing");
const themeSelect = document.getElementById("themeSelect");

function addBubble(text,type){
  const welcome = document.getElementById("welcome");
  if(welcome){ welcome.remove(); }

  const bubble = document.createElement("div");
  bubble.className = "bubble " + type;
  bubble.textContent = text;

  log.insertBefore(bubble, typing);
  log.scrollTop = log.scrollHeight;
}

function clearChat(){
  log.innerHTML = `
    <div class="welcome" id="welcome">
      <h1>Hey, I’m SpringBot 🌿</h1>
      <p>History cleared. What do you want to talk about?</p>
    </div>
    <div class="typing" id="typing">SpringBot is thinking...</div>
  `;
}

function applyTheme(theme){
  if(theme === "default"){
    document.body.removeAttribute("data-theme");
  }else{
    document.body.setAttribute("data-theme", theme);
  }
  localStorage.setItem("spring-chat-theme", theme);
}

themeSelect.addEventListener("change", function(){
  applyTheme(themeSelect.value);
});

window.addEventListener("load", function(){
  const saved = localStorage.getItem("spring-chat-theme") || "default";
  themeSelect.value = saved;
  applyTheme(saved);
});

form.addEventListener("submit", async function(e){
  e.preventDefault();

  const message = input.value.trim();
  if(!message) return;

  addBubble(message, "user");
  input.value = "";

  typing.classList.add("show");

  try{
    const response = await fetch("/api/chat", {
      method:"POST",
      headers:{
        "Content-Type":"application/json"
      },
      body:JSON.stringify({
        message:message
      })
    });

    const data = await response.json();

    typing.classList.remove("show");

    addBubble(
      data.reply || "I’m here, but I couldn’t read that response.",
      "bot"
    );

  }catch(error){

    typing.classList.remove("show");

    addBubble(
      "Connection issue. The frontend works, but the backend API did not respond.",
      "bot"
    );

  }
});

</script>

</body>
</html>

    """)


# =========================
# API ROUTES
# =========================

@app.post("/api/chat")
async def api_chat(payload: ChatRequest):

    message = payload.message.strip()

    if not message:
        return {
            "reply": "Talk to me. What’s on your mind?"
        }

    if len(message) > 1200:
        return {
            "reply": "That message is a little long. Break it down for me and I’ll help piece by piece."
        }

    reply = await generate_reply(message)

    return {
        "reply": reply
    }


@app.get("/discord")
async def discord_page():

    return HTMLResponse("""

<!DOCTYPE html>
<html>
<head>
<title>SpringBot Discord</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{
  margin:0;
  font-family:Arial,sans-serif;
  background:#050816;
  color:white;
  display:grid;
  place-items:center;
  min-height:100vh;
  text-align:center;
  padding:24px;
}
.card{
  max-width:700px;
  padding:40px;
  border-radius:28px;
  background:rgba(255,255,255,.08);
  border:1px solid rgba(255,255,255,.12);
  backdrop-filter:blur(24px);
}
a{
  display:inline-block;
  margin-top:24px;
  padding:16px 24px;
  border-radius:18px;
  background:linear-gradient(135deg,#8b5cf6,#06b6d4);
  color:white;
  text-decoration:none;
  font-weight:800;
}
</style>
</head>
<body>
<div class="card">
<h1>SpringBot Discord</h1>
<p>
Discord integration is ready to configure.
Next step is connecting Discord OAuth, bot invite,
server dashboard settings, and command controls.
</p>
<a href="/">Back Home</a>
</div>
</body>
</html>

    """)


@app.get("/health")
async def health():

    return {
        "status": "online",
        "service": "Spring Virtual Office"
    }