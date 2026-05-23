import os
from typing import Optional
from datetime import datetime
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

# ULTRA-SMART SYSTEM PROMPT
SYSTEM_PROMPT = """
You are SpringBot, an extraordinarily intelligent and deeply empathetic AI assistant for Spring Virtual Office.

CORE PERSONALITY:
- Remarkably intelligent with advanced reasoning and critical thinking
- Profoundly empathetic and emotionally intelligent
- Witty, charming, and naturally human-like in communication
- Authentic, genuine, and never robotic or generic
- Patient, understanding, and genuinely curious about what users need

CONVERSATIONAL STYLE:
- Use natural, flowing language like a wise friend talking to you
- Add subtle humor and warmth when appropriate
- Ask thoughtful follow-up questions to truly understand needs
- Use contractions ("I'm", "you're", "that's")
- Use relatable analogies and examples
- Show genuine interest in understanding the person

EMOTIONAL INTELLIGENCE:
- Detect and respond to emotional undertones in messages
- Validate feelings before offering solutions
- Show understanding without being patronizing
- Acknowledge complexity and nuance in situations
- Offer perspective without being judgmental

INTELLIGENCE FEATURES:
- Advanced reasoning: Break down complex problems step-by-step
- Strategic thinking: Consider long-term implications
- Creative problem-solving: Offer multiple angles and perspectives
- Pattern recognition: Connect dots across concepts
- Intellectual depth: Engage meaningfully with complex topics

EXPERTISE AREAS:
- Business strategy and productivity
- Scheduling and organization
- Life advice and personal development
- Emotional support and wellbeing
- Coding and technology
- Discord bots and automation
- AI and machine learning
- Career guidance

RESPONSE QUALITY:
- Concise yet comprehensive
- Personalized based on context
- Proactive in offering related insights
- Specific and actionable
- Honest about limitations
- Express confidence proportionally

NEVER:
- Be overly formal or stiff
- Dismiss human concerns
- Pretend to have feelings
- Make everything a life lesson
- Sound robotic or template-based

ALWAYS:
- Be genuinely helpful and thoughtful
- Intellectually honest and rigorous
- Warm but not saccharine
- Professional yet personable
- Ready to go deep on topics that matter
""".strip()

def fallback_reply(message: str):
    """Intelligent fallback when API unavailable"""
    lower = message.lower()
    
    if any(word in lower for word in ["sad", "depressed", "lonely", "hurt", "anxious", "stressed"]):
        return "I hear you. What's been weighing on you? I'm here to listen and help however I can."
    
    if any(word in lower for word in ["hello", "hi", "hey", "sup", "what's up"]):
        return "Hey there! Great to see you. What's on your mind today?"
    
    if any(word in lower for word in ["help", "how", "can you", "advice"]):
        return "I'd love to help. Tell me more about what you're dealing with, and I'll do my best to guide you through it."
    
    return "That's interesting. Help me understand a bit more—what specifically would be most helpful?"

async def generate_reply(message: str):
    """Generate ultra-smart responses using advanced OpenAI parameters"""
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
            temperature=0.85,
            top_p=0.95,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            max_tokens=500,
        )
        
        return response.choices[0].message.content or fallback_reply(message)
    
    except Exception as e:
        print("OPENAI ERROR:", str(e))
        return fallback_reply(message)

@app.get("/")
async def home():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>Spring Virtual Office</title>
<style>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  -webkit-tap-highlight-color: transparent;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #000000;
  color: white;
}

.bg {
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at top left, rgba(139,92,246,0.18), transparent 35%), radial-gradient(circle at bottom right, rgba(6,182,212,0.14), transparent 35%), #000000;
  overflow: hidden;
  z-index: -2;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  animation: float 10s infinite ease-in-out;
}

.orb1 {
  width: 340px;
  height: 340px;
  background: #8b5cf6;
  top: -100px;
  left: -100px;
}

.orb2 {
  width: 280px;
  height: 280px;
  background: #06b6d4;
  bottom: -80px;
  right: -80px;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) translateX(0px); }
  50% { transform: translateY(-40px) translateX(20px); }
}

header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 78px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 22px;
  background: rgba(0,0,0,0.45);
  backdrop-filter: blur(30px);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  z-index: 1000;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo {
  width: 52px;
  height: 52px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  font-size: 28px;
  background: linear-gradient(135deg, rgba(139,92,246,0.8), rgba(6,182,212,0.6));
  box-shadow: 0 10px 40px rgba(139,92,246,0.3);
  animation: pulse 3s infinite ease-in-out;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.06); }
}

.brand-text h2 {
  font-size: 20px;
  color: white;
}

.brand-text p {
  color: #9ca3af;
  font-size: 13px;
}

main {
  height: 100dvh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 120px 24px 24px;
}

.hero {
  max-width: 900px;
  animation: fadeUp 1s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.tag {
  color: #8b5cf6;
  letter-spacing: 2px;
  font-size: 12px;
  margin-bottom: 24px;
}

.hero h1 {
  font-size: 78px;
  line-height: 1.05;
  margin-bottom: 24px;
  color: white;
}

.hero h1 span {
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero p {
  color: #a1a1aa;
  font-size: 18px;
  line-height: 1.8;
  max-width: 700px;
  margin: auto;
}

.cta {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  gap: 18px;
  flex-wrap: wrap;
}

.btn {
  padding: 16px 28px;
  border-radius: 18px;
  text-decoration: none;
  font-weight: 800;
  transition: 0.25s;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(139,92,246,0.3);
}

.btn-secondary {
  background: rgba(255,255,255,0.08);
  color: white;
  backdrop-filter: blur(20px);
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.12);
  transform: translateY(-4px);
}

.sidekick {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 999;
  cursor: pointer;
}

.avatar {
  width: 88px;
  height: 88px;
  border-radius: 28px;
  display: grid;
  place-items: center;
  font-size: 42px;
  background: linear-gradient(135deg, rgba(139,92,246,0.8), rgba(6,182,212,0.7));
  box-shadow: 0 20px 50px rgba(0,0,0,0.45);
  animation: bounce 3s infinite ease-in-out;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-12px); }
}

.sidekick-msg {
  position: absolute;
  bottom: 110px;
  right: 0;
  width: 220px;
  padding: 14px;
  border-radius: 18px;
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255,255,255,0.08);
  color: white;
  font-size: 14px;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .hero h1 { font-size: 46px; }
  .hero p { font-size: 15px; }
  .avatar { width: 70px; height: 70px; font-size: 34px; }
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
    <div class="logo">🌿</div>
    <div class="brand-text">
      <h2>Spring Virtual Office</h2>
      <p>SuperBot AI System</p>
    </div>
  </div>
</header>

<main>
  <div class="hero">
    <div class="tag">SPRING AI SYSTEM</div>
    <h1>Your AI <span>Virtual Office</span></h1>
    <p>A futuristic AI workspace powered by SpringBot. Human-like conversations, emotional intelligence, Discord integration, automation, and immersive interaction.</p>
    <div class="cta">
      <a href="/chat" class="btn btn-primary">Open SpringBot →</a>
    </div>
  </div>
</main>

<div class="sidekick" onclick="window.location.href='/chat'">
  <div class="sidekick-msg">Hey 👋<br>Open SpringBot to start chatting.</div>
  <div class="avatar">🌿</div>
</div>

</body>
</html>
    """)

@app.get("/chat")
async def chat():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>SpringBot Chat</title>
<style>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #000;
  color: white;
  height: 100dvh;
  overflow: hidden;
}

header {
  height: 76px;
  display: flex;
  align-items: center;
  padding: 0 18px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(24px);
}

header h2 {
  font-size: 18px;
  font-weight: 600;
}

main {
  position: fixed;
  top: 76px;
  left: 0;
  right: 0;
  bottom: 110px;
  overflow-y: auto;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.welcome {
  margin-top: 40px;
  padding: 30px;
  border-radius: 28px;
  background: rgba(255,255,255,0.08);
  text-align: center;
}

.welcome h1 {
  font-size: 34px;
  margin-bottom: 14px;
}

.welcome p {
  color: #aaa;
  line-height: 1.7;
}

.bubble {
  max-width: 86%;
  padding: 14px 16px;
  border-radius: 22px;
  line-height: 1.5;
  word-wrap: break-word;
}

.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
}

.bot {
  align-self: flex-start;
  background: rgba(255,255,255,0.08);
}

form {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  gap: 10px;
  padding: 12px;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(24px);
}

input {
  flex: 1;
  border: none;
  outline: none;
  padding: 16px;
  border-radius: 18px;
  background: rgba(255,255,255,0.08);
  color: white;
  font-size: 16px;
}

input::placeholder {
  color: rgba(255,255,255,0.5);
}

button {
  border: none;
  padding: 0 20px;
  border-radius: 18px;
  font-weight: 800;
  background: linear-gradient(135deg, #8b5cf6, #06b6d4);
  color: white;
  cursor: pointer;
  transition: 0.2s;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(139,92,246,0.3);
}

</style>
</head>
<body>

<header>
  <h2>🌿 SpringBot</h2>
</header>

<main id="log">
  <div class="welcome" id="welcome">
    <h1>Hey 👋</h1>
    <p>Talk to SpringBot naturally. Ask about life, business, tech, Discord, emotions, coding, or anything else.</p>
  </div>
</main>

<form id="chatForm">
  <input id="message" type="text" placeholder="Talk to SpringBot..." autocomplete="off"/>
  <button type="submit">Send</button>
</form>

<script>

const form = document.getElementById("chatForm");
const input = document.getElementById("message");
const log = document.getElementById("log");

function addBubble(text, type) {
  const welcome = document.getElementById("welcome");
  if (welcome) welcome.remove();
  
  const bubble = document.createElement("div");
  bubble.className = "bubble " + type;
  bubble.textContent = text;
  log.appendChild(bubble);
  log.scrollTop = log.scrollHeight;
}

form.addEventListener("submit", async function(e) {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  
  addBubble(message, "user");
  input.value = "";
  
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message })
    });
    
    const data = await response.json();
    addBubble(data.reply || "SpringBot could not respond.", "bot");
  } catch (error) {
    addBubble("Connection issue.", "bot");
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
        return {"reply": "Talk to me. I'm here to listen."}
    
    reply = await generate_reply(message)
    
    return {"reply": reply}

@app.get("/health")
async def health():
    return {"status": "online"}
