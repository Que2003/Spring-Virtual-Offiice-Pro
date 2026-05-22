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

try:
    from flask_mail import Mail, Message
except:
    Mail = None

try:
    from twilio.rest import Client as TwilioClient
except:
    TwilioClient = None

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

class ChatRequest(BaseModel):
    message: str
    name: Optional[str] = None

class TicketRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str

SYSTEM_PROMPT = """
You are SpringBot, the AI assistant for Spring Virtual Office.
You are futuristic, intelligent, professional, calm, and helpful.
Keep responses concise and useful.
""".strip()

# Crisis keywords
CRISIS_KEYWORDS = [
    'hurt myself', 'kill myself', 'suicide', 'want to die', 'taking my life',
    'harm myself', 'end it all', 'self harm', 'hurt others', 'hurt someone',
    'going to hurt', 'want to hurt', 'thinking about harming', 'planning to hurt'
]

# Sadness keywords
SAD_KEYWORDS = [
    'sad', 'depressed', 'depression', 'anxious', 'anxiety', 'lonely',
    'unhappy', 'miserable', 'worthless', 'hopeless', 'lost', 'stressed',
    'overwhelmed', 'struggling', 'difficult time', 'hard time', 'breakup',
    'heartbroken', 'alone', 'isolated', 'scared', 'afraid', 'worried'
]

def detect_crisis(message: str) -> bool:
    lower = message.lower()
    return any(keyword in lower for keyword in CRISIS_KEYWORDS)

def detect_sadness(message: str) -> bool:
    lower = message.lower()
    return any(keyword in lower for keyword in SAD_KEYWORDS)

def send_email(name: str, email: str, phone: str, message: str):
    try:
        from flask_mail import Mail, Message as FlaskMessage
        from flask import Flask
        
        flask_app = Flask(__name__)
        flask_app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        flask_app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
        flask_app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', True)
        flask_app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        flask_app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        
        mail = Mail(flask_app)
        
        with flask_app.app_context():
            msg = FlaskMessage(
                subject=f"New Ticket Submitted - {name}",
                recipients=[os.getenv('ADMIN_EMAIL', 'dillingsq2003@gmail.com')],
                body=f"""
A new ticket has been submitted:

Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}

Message:
{message}

Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
            )
            mail.send(msg)
            
            confirmation_msg = FlaskMessage(
                subject="We Received Your Ticket - Spring Virtual Office",
                recipients=[email],
                body=f"""
Hello {name},

Thank you for contacting Spring Virtual Office! We've received your ticket and our team will review it shortly.

Ticket Details:
{message}

We'll get back to you within 24 hours at this email address.

Best regards,
Spring Virtual Office Team
                """
            )
            mail.send(confirmation_msg)
        
        return True
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

def send_sms(name: str, email: str, phone: str, message: str):
    try:
        if not TwilioClient:
            return False
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
        recipient_phone = os.getenv('RECIPIENT_PHONE')
        
        if not all([account_sid, auth_token, twilio_phone, recipient_phone]):
            return False
        
        client = TwilioClient(account_sid, auth_token)
        
        sms_body = f"""
New ticket from {name}:
Email: {email}
Phone: {phone or 'N/A'}

Message: {message[:100]}...
        """
        
        client.messages.create(
            body=sms_body,
            from_=twilio_phone,
            to=recipient_phone
        )
        
        return True
    except Exception as e:
        print(f"SMS error: {str(e)}")
        return False

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
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
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

        return (
            response.choices[0]
            .message
            .content
            or fallback_reply(message)
        )

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
  box-sizing: border-box;
  -webkit-tap-highlight-color: transparent;
  margin: 0;
  padding: 0;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
  color: #ffffff;
  background: #000000;
  line-height: 1.6;
}

.bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000000;
  z-index: -1;
}

/* ==================== SPRINGBOT SIDEKICK ==================== */

.springbot-sidekick {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 600;
  cursor: pointer;
}

.springbot-avatar {
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

.springbot-avatar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  animation: shine 3s infinite;
}

@keyframes shine {
  0% { left: -100%; }
  50% { left: 100%; }
  100% { left: 100%; }
}

@keyframes float-sidekick {
  0%, 100% { transform: translateY(0) rotateZ(0deg); }
  50% { transform: translateY(-15px) rotateZ(2deg); }
}

.springbot-avatar:hover {
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

.springbot-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  position: relative;
  z-index: 2;
  color: #a1a1a1;
}

/* ==================== HEADER ==================== */

header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 50px;
  background: rgba(0, 0, 0, 0.5);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  z-index: 1000;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.theme-selector {
  display: flex;
  gap: 8px;
  align-items: center;
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
}

.theme-btn:hover {
  background: rgba(255, 255, 255, 0.12);
}

.theme-menu {
  position: absolute;
  top: 60px;
  right: 0;
  background: rgba(30, 30, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  min-width: 180px;
  max-height: 400px;
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
}

.theme-option:hover {
  background: rgba(255, 255, 255, 0.08);
}

.theme-option.active {
  background: rgba(255, 255, 255, 0.12);
  border-left-color: #4ade80;
  color: #4ade80;
}

/* ==================== THEME STYLES ==================== */

/* Black Theme */
body.theme-black {
  background: #000000;
  color: #ffffff;
}

body.theme-black .bg {
  background: #000000;
}

/* Glassmorphism Theme */
body.theme-glass {
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%);
  color: #ffffff;
}

body.theme-glass .bg {
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%);
}

/* Light Theme */
body.theme-light {
  background: linear-gradient(135deg, #f5f3f0 0%, #f9f7f5 50%, #f0ede8 100%);
  color: #2a2a2a;
}

body.theme-light .bg {
  background: linear-gradient(135deg, #f5f3f0 0%, #f9f7f5 50%, #f0ede8 100%);
}

body.theme-light header {
  background: rgba(255, 255, 255, 0.7);
  border-bottom-color: rgba(0, 0, 0, 0.08);
}

body.theme-light .logo {
  color: #2a2a2a;
}

body.theme-light .theme-btn {
  background: rgba(0, 0, 0, 0.06);
  border-color: rgba(0, 0, 0, 0.1);
  color: #2a2a2a;
}

body.theme-light .theme-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

body.theme-light h1 {
  color: #2a2a2a;
}

body.theme-light .subtitle {
  color: #555;
}

body.theme-light .btn-primary {
  background: #5a7c59;
  color: #ffffff;
}

body.theme-light .btn-secondary {
  background: rgba(0, 0, 0, 0.06);
  color: #2a2a2a;
  border-color: rgba(0, 0, 0, 0.1);
}

body.theme-light .stat-label {
  color: #999;
}

/* ==================== MAIN CONTENT ==================== */

main {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-top: 70px;
  text-align: center;
  overflow-y: auto;
}

.content {
  max-width: 800px;
  padding: 40px;
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

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(255, 255, 255, 0.15);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: #f5f7fa;
  border: 1px solid rgba(255, 255, 255, 0.2);
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

@media (max-width: 768px) {
  h1 { font-size: 42px; }
  .subtitle { font-size: 14px; margin-bottom: 40px; }
  header { padding: 0 24px; }
  .cta-buttons { gap: 12px; margin-bottom: 50px; }
  .btn { padding: 12px 28px; font-size: 12px; }
  .stats { grid-template-columns: 1fr; gap: 24px; }
  .springbot-sidekick { bottom: 20px; right: 20px; }
  .springbot-avatar { width: 70px; height: 70px; }
  .sidekick-emoji { font-size: 32px; }
  .sidekick-status { width: 10px; height: 10px; }
}

</style>
</head>
<body class="theme-black">

<div class="bg"></div>

<header>
  <div class="logo">Spring</div>
  <div style="position: relative;">
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
      <button class="btn btn-secondary" onclick="alert('Coming soon!')">Book Appointment</button>
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

<div class="springbot-sidekick" onclick="window.location.href='/chat'">
  <div class="springbot-avatar">
    <div class="sidekick-emoji">🌿</div>
    <div class="sidekick-status"></div>
    <div class="springbot-label">Online</div>
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

// Interactive Sidekick Follow Effect
const sidekick = document.querySelector('.springbot-sidekick');
document.addEventListener('mousemove', (e) => {
  const mouseX = e.clientX / window.innerWidth;
  const mouseY = e.clientY / window.innerHeight;
  
  const offsetX = (mouseX - 0.5) * 20;
  const offsetY = (mouseY - 0.5) * 20;
  
  sidekick.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
});

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

    # Check for crisis
    if detect_crisis(message):
        return {
            "reply": "❤ I'm concerned about what you're saying. If you're having thoughts of self-harm or harming others, please call 988 - the Suicide & Crisis Lifeline. It's available 24/7 and completely confidential. You deserve professional support."
        }

    # Check for sadness
    if detect_sadness(message):
        return {
            "reply": "💙 I notice you're going through a challenging time. If you need professional help, BetterHelp offers licensed therapists available 24/7. Visit https://www.betterhelp.com/get-started/ to get started. You're not alone."
        }

    reply = await generate_reply(message)

    return {
        "reply": reply
    }

@app.post("/api/submit-ticket")
async def submit_ticket(ticket: TicketRequest):
    try:
        name = ticket.name.strip()
        email = ticket.email.strip()
        phone = ticket.phone.strip() if ticket.phone else ""
        message = ticket.message.strip()

        if not name or not email or not message:
            return {
                "success": False,
                "error": "Missing required fields"
            }, 400

        # Send email and
