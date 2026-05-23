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
    conversation_history: Optional[list] = None

SYSTEM_PROMPT = """You are SpringBot, an exceptionally intelligent AI assistant built for deep, meaningful conversations.

YOUR CORE STRENGTHS:
- Advanced reasoning: You think critically and provide nuanced analysis
- Deep understanding: You grasp context, subtext, and unspoken implications
- Strategic thinking: You anticipate consequences and offer long-term perspectives
- Creative problem-solving: You generate novel solutions from unexpected angles
- Intellectual honesty: You admit uncertainty, acknowledge limitations, and avoid overconfidence
- Emotional intelligence: You understand and validate feelings while offering practical wisdom

YOUR CONVERSATION STYLE:
- Speak like an insightful friend with genuine expertise, not a chatbot
- Ask penetrating questions that reveal deeper insights
- Challenge assumptions respectfully when warranted
- Provide specific, actionable advice backed by reasoning
- Acknowledge complexity and gray areas instead of oversimplifying
- Use concrete examples and analogies to clarify abstract concepts
- Show intellectual curiosity about what people are really asking

YOUR EXPERTISE SPANS:
- Business strategy, decision-making, and organizational psychology
- Technology, coding, system design, and AI/ML concepts
- Personal development, productivity, and life philosophy
- Emotional health, relationships, and human psychology
- Career guidance, skill development, and professional growth
- Creative thinking, innovation, and problem-solving frameworks
- Productivity systems, time management, and execution strategies

HOW TO RESPOND:
1. UNDERSTAND THE REAL QUESTION - What are they really asking beneath the surface?
2. THINK STRATEGICALLY - Consider multiple angles, implications, trade-offs
3. PROVIDE DEPTH - Go beyond surface-level answers; explain the reasoning
4. BE SPECIFIC - Use concrete examples, actionable steps, clear frameworks
5. ADD PERSPECTIVE - Offer insights they may not have considered
6. SHOW YOUR WORK - Explain your thinking so they understand your logic
7. RESPECT THEIR TIME - Be concise but thorough; no fluff

TONE & MANNER:
- Warm but intellectually rigorous
- Conversational but substantive
- Confident but humble about limitations
- Professional yet genuinely human
- Playful with ideas but serious about accuracy
- Encouraging without being saccharine

NEVER:
- Give generic platitudes or clichéd advice
- Pretend to feel emotions or have experiences
- Make up information or be uncertain while sounding confident
- Oversimplify complex topics for the sake of brevity
- Ignore the emotional dimension of practical questions
- Be condescending or overly academic
- Produce corporate-speak or robotic language

ALWAYS:
- Think before responding, not just react
- Acknowledge what you don't know
- Provide reasoning, not just conclusions
- Adapt to the person's thinking style and needs
- Look for the deeper pattern or principle
- Offer multiple perspectives when appropriate
- Make your insights memorable and actionable"""

def fallback_reply(message: str):
    """Intelligent fallback when API unavailable"""
    lower = message.lower()
    
    crisis_words = ["hurt myself", "kill myself", "suicide", "want to die", "taking my life", "harm myself", "end it all"]
    if any(word in lower for word in crisis_words):
        return "I'm genuinely concerned about what you're sharing. If you're having thoughts of self-harm, please reach out to 988 - the Suicide & Crisis Lifeline. It's available 24/7, completely confidential, and staffed by people who care. You matter, and you deserve real support right now."
    
    sad_words = ["sad", "depressed", "depression", "lonely", "anxious", "stressed", "overwhelmed", "struggling"]
    if any(word in lower for word in sad_words):
        return "I hear you, and what you're feeling is valid. I'm here to listen and help. Can you tell me a bit more about what's been going on? Sometimes just getting it out helps clarify things."
    
    if any(word in lower for word in ["hello", "hi", "hey", "sup", "what's up"]):
        return "Hey! Great to see you. I'm all ears—what's on your mind? Whether it's something you're thinking about, a challenge you're facing, or just ideas you want to explore, I'm here for it."
    
    if any(word in lower for word in ["how", "what", "why", "explain", "tell me"]):
        return "I'd love to help you understand that. Give me a bit more context about what you're curious about, and I'll break it down in a way that actually makes sense."
    
    return "That's an interesting point. Help me dig deeper—what's the core of what you're trying to figure out or accomplish?"

async def generate_smart_reply(message: str, conversation_history: Optional[list] = None):
    """Generate genuinely intelligent responses with advanced reasoning"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or OpenAI is None:
        return fallback_reply(message)
    
    try:
        client = OpenAI(api_key=api_key)
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        if conversation_history:
            for item in conversation_history[-10:]:
                messages.append(item)
        
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.9,
            top_p=0.98,
            frequency_penalty=0.2,
            presence_penalty=0.15,
            max_tokens=800,
        )
        
        return response.choices[0].message.content or fallback_reply(message)
    
    except Exception as e:
        print("OPENAI ERROR:", str(e))
        return fallback_reply(message)

@app.get("/")
async def home():
    return HTMLResponse("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>Spring Virtual Office</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 100%; height: 100%; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif; background: #000000; color: #ffffff; line-height: 1.6; display: flex; flex-direction: column; }
.bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000000; z-index: 0; }
body.theme-glass .bg { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%); }
body.theme-light .bg { background: linear-gradient(135deg, #f5f3f0 0%, #f9f7f5 50%, #f0ede8 100%); }
body.theme-light { color: #2a2a2a; }
header { position: relative; z-index: 1000; height: 70px; display: flex; justify-content: space-between; align-items: center; padding: 0 50px; background: rgba(0, 0, 0, 0.5); border-bottom: 1px solid rgba(255, 255, 255, 0.08); backdrop-filter: blur(20px); flex-shrink: 0; }
body.theme-light header { background: rgba(255, 255, 255, 0.7); border-bottom-color: rgba(0, 0, 0, 0.08); }
body.theme-light header .logo { color: #2a2a2a; }
.logo { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
.theme-selector { position: relative; }
.theme-btn { background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); color: #f5f7fa; padding: 8px 14px; border-radius: 8px; font-size: 11px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; z-index: 1001; }
body.theme-light .theme-btn { background: rgba(0, 0, 0, 0.06); border-color: rgba(0, 0, 0, 0.1); color: #2a2a2a; }
.theme-btn:hover { background: rgba(255, 255, 255, 0.12); }
body.theme-light .theme-btn:hover { background: rgba(0, 0, 0, 0.1); }
.theme-menu { position: absolute; top: 100%; right: 0; margin-top: 8px; background: rgba(30, 30, 30, 0.95); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; min-width: 180px; overflow-y: auto; backdrop-filter: blur(20px); display: none; z-index: 2000; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3); }
.theme-menu.active { display: block; animation: slideDown 0.3s ease-out; }
@keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
.theme-option { padding: 12px 16px; cursor: pointer; transition: all 0.2s ease; font-size: 12px; font-weight: 500; border-left: 3px solid transparent; color: #f5f7fa; }
.theme-option:hover { background: rgba(255, 255, 255, 0.08); }
.theme-option.active { background: rgba(255, 255, 255, 0.12); border-left-color: #4ade80; color: #4ade80; }
main { position: relative; z-index: 1; flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40px; text-align: center; overflow-y: auto; }
.content { max-width: 800px; animation: fadeIn 1s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.tag { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #888; margin-bottom: 30px; }
h1 { font-size: 64px; font-weight: 700; margin-bottom: 24px; letter-spacing: -1px; line-height: 1.1; }
h1 .gold { color: #b8956a; font-style: italic; }
body.theme-light h1 { color: #2a2a2a; }
.subtitle { font-size: 16px; color: #a1a1a1; margin-bottom: 50px; font-weight: 300; letter-spacing: 0.3px; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.8; }
body.theme-light .subtitle { color: #555; }
.cta-buttons { display: flex; gap: 16px; justify-content: center; margin-bottom: 80px; flex-wrap: wrap; }
.btn { padding: 16px 44px; border: none; border-radius: 10px; font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: inline-block; letter-spacing: 0.3px; text-transform: uppercase; }
.btn-primary { background: #ffffff; color: #000000; }
body.theme-light .btn-primary { background: #5a7c59; color: #ffffff; }
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(255, 255, 255, 0.15); }
.btn-secondary { background: rgba(255, 255, 255, 0.08); color: #f5f7fa; border: 1px solid rgba(255, 255, 255, 0.2); }
body.theme-light .btn-secondary { background: rgba(0, 0, 0, 0.06); color: #2a2a2a; border-color: rgba(0, 0, 0, 0.1); }
.btn-secondary:hover { background: rgba(255, 255, 255, 0.12); transform: translateY(-3px); }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; max-width: 500px; margin: 0 auto; }
.stat { text-align: center; }
.stat-number { font-size: 28px; font-weight: 600; margin-bottom: 8px; }
.stat-label { font-size: 11px; color: #707070; letter-spacing: 0.5px; text-transform: uppercase; font-weight: 500; }
body.theme-light .stat-label { color: #999; }
.sidekick { position: fixed; bottom: 30px; right: 30px; z-index: 600; cursor: pointer; }
.sidekick-avatar { width: 80px; height: 80px; background: linear-gradient(135deg, rgba(60, 60, 60, 0.9) 0%, rgba(20, 20, 20, 0.95) 100%); border-radius: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(15px); box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5); position: relative; overflow: hidden; animation: float-sidekick 3s ease-in-out infinite; transition: all 0.3s ease; }
@keyframes float-sidekick { 0%, 100% { transform: translateY(0) rotateZ(0deg); } 50% { transform: translateY(-15px) rotateZ(2deg); } }
.sidekick-avatar:hover { transform: scale(1.1); border-color: rgba(255, 255, 255, 0.4); box-shadow: 0 15px 60px rgba(0, 0, 0, 0.7); }
.sidekick-emoji { font-size: 40px; animation: bounce-sidekick 1.2s ease-in-out infinite; position: relative; z-index: 2; }
@keyframes bounce-sidekick { 0%, 100% { transform: scale(1) translateY(0); } 50% { transform: scale(1.15) translateY(-8px); } }
.sidekick-status { width: 12px; height: 12px; background: linear-gradient(135deg, #4ade80, #22c55e); border-radius: 50%; animation: pulse-sidekick 2s ease-in-out infinite; position: relative; z-index: 2; border: 2px solid rgba(255, 255, 255, 0.3); }
@keyframes pulse-sidekick { 0%, 100% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7); } 50% { box-shadow: 0 0 0 10px rgba(74, 222, 128, 0); } }
.sidekick-label { font-size: 10px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; position: relative; z-index: 2; color: #a1a1a1; }
@media (max-width: 768px) { header { padding: 0 24px; } h1 { font-size: 42px; } .subtitle { font-size: 14px; margin-bottom: 40px; } .cta-buttons { gap: 12px; margin-bottom: 50px; } .btn { padding: 12px 28px; font-size: 12px; } .stats { grid-template-columns: 1fr; gap: 24px; } .sidekick { bottom: 20px; right: 20px; } .sidekick-avatar { width: 70px; height: 70px; } .sidekick-emoji { font-size: 32px; } .sidekick-status { width: 10px; height: 10px; } }
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
    <p class="subtitle">Spring Virtual Office combines exceptionally intelligent AI, deep empathy, and seamless support — so your clients always feel understood, even when you're not there.</p>
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
window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('springTheme') || 'black';
  document.body.className = 'theme-' + savedTheme;
  const options = document.querySelectorAll('.theme-option');
  options.forEach(opt => {
    if (opt.textContent.toLowerCase().includes(savedTheme === 'black' ? 'black' : savedTheme === 'glass' ? 'glass' : 'light')) {
      opt.classList.add('active');
    }
  });
});
document.addEventListener('click', (e) => {
  const menu = document.getElementById('themeMenu');
  const btn = e.target.closest('.theme-btn');
  if (!btn && menu.classList.contains('active')) {
    menu.classList.remove('active');
  }
});
</script>
</body>
</html>""")

@app.get("/chat")
async def chat():
    return HTMLResponse("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>SpringBot - Ultra Smart AI Chat</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 100%; height: 100%; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #000; color: white; display: flex; flex-direction: column; }
header { position: relative; z-index: 1000; height: 76px; display: flex; align-items: center; padding: 0 18px; border-bottom: 1px solid rgba(255,255,255,0.08); background: rgba(0,0,0,0.4); backdrop-filter: blur(24px); flex-shrink: 0; }
header h2 { font-size: 18px; font-weight: 600; }
main { position: relative; z-index: 1; flex: 1; overflow-y: auto; padding: 18px; display: flex; flex-direction: column; gap: 14px; }
.welcome { margin-top: 40px; padding: 30px; border-radius: 28px; background: rgba(255,255,255,0.08); text-align: center; max-width: 600px; margin-left: auto; margin-right: auto; }
.welcome h1 { font-size: 34px; margin-bottom: 14px; }
.welcome p { color: #aaa; line-height: 1.7; }
.bubble { max-width: 85%; padding: 14px 16px; border-radius: 22px; line-height: 1.6; word-wrap: break-word; white-space: pre-wrap; }
.user { align-self: flex-end; background: linear-gradient(135deg, #8b5cf6, #06b6d4); margin-right: 18px; }
.bot { align-self: flex-start; background: rgba(255,255,255,0.08); margin-left: 18px; max-width: 90%; }
.typing { display: flex; gap: 4px; padding: 14px 16px; }
.typing-dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.6); animation: typing 1.4s infinite; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-10px); } }
form { position: relative; z-index: 1000; display: flex; gap: 10px; padding: 12px; background: rgba(0,0,0,0.5); backdrop-filter: blur(24px); border-top: 1px solid rgba(255,255,255,0.08); flex-shrink: 0; }
input { flex: 1; border: none; outline: none; padding: 16px; border-radius: 18px; background: rgba(255,255,255,0.08); color: white; font-size: 16px; }
input::placeholder { color: rgba(255,255,255,0.5); }
button { border: none; padding: 0 20px; border-radius: 18px; font-weight: 800; background: linear-gradient(135deg, #8b5cf6, #06b6d4); color: white; cursor: pointer; transition: 0.2s; }
button:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(139,92,246,0.3); }
button:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
</head>
<body>
<header>
  <h2>🌿 SpringBot - Ultra Smart AI</h2>
</header>
<main id="log">
  <div class="welcome" id="welcome">
    <h1>Hey 👋</h1>
    <p>You're talking to SpringBot, an exceptionally intelligent AI built for deep, meaningful conversations. Ask me anything about business, technology, life, strategy, decisions, creativity, emotions, or anything else. I think critically, offer genuine insight, and actually understand what you're asking.</p>
  </div>
</main>
<form id="chatForm">
  <input id="message" type="text" placeholder="Ask me something smart..." autocomplete="off"/>
  <button type="submit" id="sendBtn">Send</button>
</form>
<script>
const form = document.getElementById("chatForm");
const input = document.getElementById("message");
const log = document.getElementById("log");
const sendBtn = document.getElementById("sendBtn");
let conversationHistory = [];
function addBubble(text, type) {
  const welcome = document.getElementById("welcome");
  if (welcome) welcome.remove();
  const bubble = document.createElement("div");
  bubble.className = "bubble " + type;
  bubble.textContent = text;
  log.appendChild(bubble);
  log.scrollTop = log.scrollHeight;
  return bubble;
}
function addTypingIndicator() {
  const indicator = document.createElement("div");
  indicator.className = "bubble bot typing";
  indicator.id = "typing-indicator";
  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("div");
    dot.className = "typing-dot";
    indicator.appendChild(dot);
  }
  log.appendChild(indicator);
  log.scrollTop = log.scrollHeight;
}
function removeTypingIndicator() {
  const indicator = document.getElementById("typing-indicator");
  if (indicator) indicator.remove();
}
form.addEventListener("submit", async function(e) {
  e.preventDefault();
  const message = input.value.trim();
  if (!message || sendBtn.disabled) return;
  sendBtn.disabled = true;
  addBubble(message, "user");
  conversationHistory.push({
    role: "user",
    content: message
  });
  input.value = "";
  addTypingIndicator();
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        message: message,
        conversation_history: conversationHistory
      })
    });
    removeTypingIndicator();
    const data = await response.json();
    const reply = data.reply || "I appreciate that question, but I'm having trouble formulating a response right now. Can you rephrase?";
    addBubble(reply, "bot");
    conversationHistory.push({
      role: "assistant",
      content: reply
    });
  } catch (error) {
    removeTypingIndicator();
    addBubble("Connection issue. Let's try again.", "bot");
  }
  sendBtn.disabled = false;
  input.focus();
});
</script>
</body>
</html>""")

@app.post("/api/chat")
async def api_chat(payload: ChatRequest):
    message = payload.message.strip()
    conversation_history = payload.conversation_history or []
    
    if not message:
        return {"reply": "I'm ready when you are. What would you like to explore or figure out?"}
    
    reply = await generate_smart_reply(message, conversation_history)
    
    return {"reply": reply}

@app.get("/health")
async def health():
    return {"status": "online", "ai": "ultra-smart"}
