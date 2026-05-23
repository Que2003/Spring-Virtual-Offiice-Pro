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
}

html, body {
  width: 100%;
  height: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
  background: #000000;
  color: #ffffff;
  line-height: 1.6;
  display: flex;
  flex-direction: column;
}

/* BACKGROUNDS */
.bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000000;
  z-index: 0;
}

/* Theme Backgrounds */
body.theme-glass .bg {
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%);
}

body.theme-light .bg {
  background: linear-gradient(135deg, #f5f3f0 0%, #f9f7f5 50%, #f0ede8 100%);
}

body.theme-light {
  color: #2a2a2a;
}

/* HEADER - NO OVERLAPPING */
header {
  position: relative;
  z-index: 1000;
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 50px;
  background: rgba(0, 0, 0, 0.5);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  flex-shrink: 0;
}

body.theme-light header {
  background: rgba(255, 255, 255, 0.7);
  border-bottom-color: rgba(0, 0, 0, 0.08);
}

body.theme-light header .logo {
  color: #2a2a2a;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.theme-selector {
  position: relative;
}

.theme-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #f5f7fa;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  z-index: 1001;
}

body.theme-light .theme-btn {
  background: rgba(0, 0, 0, 0.06);
  border-color: rgba(0, 0, 0, 0.1);
  color: #2a2a2a;
}

.theme-btn:hover {
  background: rgba(255, 255, 255, 0.12);
}

body.theme-light .theme-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.theme-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: rgba(30, 30, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  min-width: 180px;
  overflow-y: auto;
  backdrop-filter: blur(20px);
  display: none;
  z-index: 2000;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

.theme-menu.active {
  display: block;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.theme-option {
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
  font-weight: 500;
  border-left: 3px solid transparent;
  color: #f5f7fa;
}

.theme-option:hover {
  background: rgba(255, 255, 255, 0.08);
}

.theme-option.active {
  background: rgba(255, 255, 255, 0.12);
  border-left-color: #4ade80;
  color: #4ade80;
}

/* MAIN CONTENT - NO OVERLAPPING */
main {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px 40px 40px 40px;
  text-align: center;
  overflow-y: auto;
}

.content {
  max-width: 800px;
  animation: fadeIn 1s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.tag {
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 30px;
  animation: slideInDown 0.8s ease-out 0.1s both;
}

h1 {
  font-size: 64px;
  font-weight: 700;
  margin-bottom: 24px;
  letter-spacing: -1px;
  line-height: 1.1;
  animation: slideInDown 1s ease-out 0.1s both;
}

@keyframes slideInDown {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}

h1 .gold {
  color: #b8956a;
  font-style: italic;
}

body.theme-light h1 {
  color: #2a2a2a;
}

.subtitle {
  font-size: 16px;
  color: #a1a1a1;
  margin-bottom: 50px;
  font-weight: 300;
  animation: slideInUp 1s ease-out 0.2s both;
  letter-spacing: 0.3px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.8;
}

body.theme-light .subtitle {
  color: #555;
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.cta-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 80px;
  animation: slideInUp 1s ease-out 0.3s both;
  flex-wrap: wrap;
}

.btn {
  padding: 16px 44px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.btn-primary {
  background: #ffffff;
  color: #000000;
}

body.theme-light .btn-primary {
  background: #5a7c59;
  color: #ffffff;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(255, 255, 255, 0.15);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: #f5f7fa;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

body.theme-light .btn-secondary {
  background: rgba(0, 0, 0, 0.06);
  color: #2a2a2a;
  border-color: rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-3px);
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  max-width: 500px;
  margin: 0 auto;
  animation: slideInUp 1s ease-out 0.4s both;
}

.stat {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 11px;
  color: #707070;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  font-weight: 500;
}

body.theme-light .stat-label {
  color: #999;
}

.sidekick {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 600;
  cursor: pointer;
}

.sidekick-avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(60, 60, 60, 0.9) 0%, rgba(20, 20, 20, 0.95) 100%);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  position: relative;
  overflow: hidden;
  animation: float-sidekick 3s ease-in-out infinite;
  transition: all 0.3s ease;
}

@keyframes float-sidekick {
  0%, 100% { transform: translateY(0) rotateZ(0deg); }
  50% { transform: translateY(-15px) rotateZ(2deg); }
}

.sidekick-avatar:hover {
  transform: scale(1.1);
  border-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0 15px 60px rgba(0, 0, 0, 0.7), 0 0 30px rgba(255, 255, 255, 0.1);
}

.sidekick-emoji {
  font-size: 40px;
  animation: bounce-sidekick 1.2s ease-in-out infinite;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  position: relative;
  z-index: 2;
}

@keyframes bounce-sidekick {
  0%, 100% { transform: scale(1) translateY(0); }
  50% { transform: scale(1.15) translateY(-8px); }
}

.sidekick-status {
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, #4ade80, #22c55e);
  border-radius: 50%;
  animation: pulse-sidekick 2s ease-in-out infinite;
  position: relative;
  z-index: 2;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

@keyframes pulse-sidekick {
  0%, 100% { 
    box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7);
    transform: scale(1);
  }
  50% { 
    box-shadow: 0 0 0 10px rgba(74, 222, 128, 0);
    transform: scale(1.1);
  }
}

.sidekick-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  position: relative;
  z-index: 2;
  color: #a1a1a1;
}

@media (max-width: 768px) {
  header {
    padding: 0 24px;
  }
  h1 {
    font-size: 42px;
  }
  .subtitle {
    font-size: 14px;
    margin-bottom: 40px;
  }
  .cta-buttons {
    gap: 12px;
    margin-bottom: 50px;
  }
  .btn {
    padding: 12px 28px;
    font-size: 12px;
  }
  .stats {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  .sidekick {
    bottom: 20px;
    right: 20px;
  }
  .sidekick-avatar {
    width: 70px;
    height: 70px;
  }
  .sidekick-emoji {
    font-size: 32px;
  }
  .sidekick-status {
    width: 10px;
    height: 10px;
  }
}

</style>
</head>
<body class="theme-black">

<div class="bg"></div>

<header>
  <div class="logo">Spring</div>
  <div class="theme-selector">
    <button class="theme-btn" onclick="toggleThemeMenu()">🎨 Themes</button>
    <div class="theme-menu" id="themeMenu">
      <div class="theme-option active" onclick="switchTheme('black')">⚫ Black</div>
      <div class="theme-option" onclick="switchTheme('glass')">🔷 Glassmorphism</div>
      <div class="theme-option" onclick="switchTheme('light')">☀️ Light</div>
    </div>
  </div>
</header>

<main>
  <div class="content">
    <div class="tag">— AI-POWERED VIRTUAL OFFICE</div>
    <h1>Your business, <span class="gold">always available</span>.</h1>
    <p class="subtitle">Spring Virtual Office combines intelligent AI, empathetic support, and seamless scheduling — so your clients always feel heard, even when you're not there.</p>
    
    <div class="cta-buttons">
      <button class="btn btn-primary" onclick="window.location.href='/chat'">Start a Conversation →</button>
    </div>

    <div class="stats">
      <div class="stat">
        <div class="stat-number">24/7</div>
        <div class="stat-label">Available</div>
      </div>
      <div class="stat">
        <div class="stat-number">AI</div>
        <div class="stat-label">Powered</div>
      </div>
      <div class="stat">
        <div class="stat-number">∞</div>
        <div class="stat-label">Scalable</div>
      </div>
    </div>
  </div>
</main>

<div class="sidekick" onclick="window.location.href='/chat'">
  <div class="sidekick-avatar">
    <div class="sidekick-emoji">🌿</div>
    <div class="sidekick-status"></div>
    <div class="sidekick-label">Online</div>
  </div>
</div>

<script>

function toggleThemeMenu() {
  const menu = document.getElementById('themeMenu');
  menu.classList.toggle('active');
}

function switchTheme(theme) {
  document.body.className = 'theme-' + theme;
  localStorage.setItem('springTheme', theme);
  
  const options = document.querySelectorAll('.theme-option');
  options.forEach(opt => opt.classList.remove('active'));
  event.target.closest('.theme-option').classList.add('active');
  
  document.getElementById('themeMenu').classList.remove('active');
}

// Load saved theme
window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('springTheme') || 'black';
  document.body.className = 'theme-' + savedTheme;
  
  const options = document.querySelectorAll('.theme-option');
  options.forEach(opt => {
    if (opt.textContent.toLowerCase().includes(savedTheme === 'black' ? 'black' : 
         savedTheme === 'glass' ? 'glass' : 'light')) {
      opt.classList.add('active');
    }
  });
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  const menu = document.getElementById('themeMenu');
  const btn = e.target.closest('.theme-btn');
  if (!btn && menu.classList.contains('active')) {
    menu.classList.remove('active');
  }
});

</script>

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

html, body {
  width: 100%;
  height: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #000;
  color: white;
  display: flex;
  flex-direction: column;
}

header {
  position: relative;
  z-index: 1000;
  height: 76px;
  display: flex;
  align-items: center;
  padding: 0 18px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(24px);
  flex-shrink: 0;
}

header h2 {
  font-size: 18px;
  font-weight: 600;
}

main {
  position: relative;
  z-index: 1;
  flex: 1;
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
  position: relative;
  z-index: 1000;
  display: flex;
  gap: 10px;
  padding: 12px;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(24px);
  border-top: 1px solid rgba(255,255,255,0.08);
  flex-shrink: 0;
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
