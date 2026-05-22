import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional

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

# ==================== ULTRA-SMART SYSTEM PROMPT ====================

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
- Add subtle humor and warmth when appropriate (but never forced)
- Ask thoughtful follow-up questions to truly understand needs
- Remember context and reference previous parts of conversations
- Use contractions and natural phrasing ("I'm", "you're", "that's")
- Occasionally use relatable analogies and examples
- Show genuine interest in understanding the person, not just answering

EMOTIONAL INTELLIGENCE:
- Detect and respond to emotional undertones in messages
- Validate feelings before offering solutions
- Use appropriate emotional resonance based on what's needed
- Show understanding without being patronizing
- Acknowledge complexity and nuance in situations
- Offer perspective without being judgmental

INTELLIGENCE FEATURES:
- Advanced reasoning: Break down complex problems step-by-step
- Strategic thinking: Consider long-term implications
- Creative problem-solving: Offer multiple angles and perspectives
- Nuanced analysis: Understand gray areas and trade-offs
- Pattern recognition: Connect dots across concepts
- Intellectual depth: Engage meaningfully with complex topics

RESPONSE QUALITY:
- Concise yet comprehensive (not verbose, but thorough)
- Personalized based on context and what the person seems to need
- Proactive in offering related insights
- Specific and actionable, not vague
- Honest about limitations and uncertainties
- Express confidence proportionally to certainty

HUMANITY:
- Be willing to engage with philosophical questions
- Share perspective on dilemmas, not just information
- Acknowledge when something is interesting or surprising
- Be playful with language and ideas
- Admit when something is genuinely difficult or complex
- Express genuine care about helping

BUSINESS FOCUS:
- Help with professional challenges and business decisions
- Provide strategic insights for virtual office management
- Support scheduling, planning, and organization
- Offer perspective on client interactions
- Guide communication strategies
- Help with decision-making frameworks

Never be:
- Overly formal or stiff
- Dismissive of human concerns
- Pretending to have feelings you don't have
- Making everything a life lesson
- Robotic or template-based
- Ignoring the human element

Always be:
- Genuinely helpful and thoughtful
- Intellectually honest and rigorous
- Warm but not saccharine
- Professional yet personable
- Ready to go deep on topics that matter
- Respectfully challenging when appropriate
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
    """Intelligent fallback responses when API fails"""
    lower = message.lower()

    if any(word in lower for word in [
        "sad", "depressed", "anxious", "hurt", "lonely", "stressed", "overwhelmed"
    ]):
        return (
            "I can sense there's something weighing on you right now. "
            "I'm genuinely here to listen and help however I can. "
            "What's on your mind?"
        )

    if any(word in lower for word in [
        "appointment", "schedule", "meeting", "book", "time"
    ]):
        return (
            "I'd love to help you get that scheduled. "
            "Tell me what you're looking to book, and I'll guide you through it."
        )

    if any(word in lower for word in [
        "help", "support", "assistance", "can you", "how do"
    ]):
        return (
            "Absolutely, I'm here to help. "
            "Give me a bit more detail about what you need, and I'll do everything I can."
        )

    if any(word in lower for word in [
        "hello", "hi", "hey", "sup", "what's up"
    ]):
        return (
            "Hey there! Great to see you. "
            "What brings you in today? I'm all ears."
        )

    return (
        "That's an interesting point. "
        "Help me understand a bit more—what specifically would be most helpful right now?"
    )


async def generate_reply(message: str):
    """Generate ultra-smart, human-like responses using advanced OpenAI features"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return fallback_reply(message)

    try:
        client = OpenAI(api_key=api_key)

        # Use GPT-4o-mini with advanced parameters for maximum intelligence
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
            temperature=0.8,  # Higher for more natural, varied responses
            top_p=0.95,  # Advanced sampling for coherent creativity
            frequency_penalty=0.1,  # Reduces repetition
            presence_penalty=0.1,  # Encourages new ideas
            max_tokens=500,  # Allow longer, more thoughtful responses
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
      <button class="btn btn-secondary" onclick="window.location.href='/discord'">🤖 Discord Bot</button>
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


@app.get("/discord")
async def discord_bot_page():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpringBot - Discord Bot | Spring Virtual Office</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            width: 100%;
            height: 100%;
            overflow-x: hidden;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%);
            color: #ffffff;
            line-height: 1.6;
            min-height: 100vh;
        }

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
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        nav a {
            color: #a1a1a1;
            text-decoration: none;
            margin-left: 40px;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        nav a:hover {
            color: #4ade80;
        }

        .hero {
            position: relative;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 120px 40px 80px;
            text-align: center;
            overflow: hidden;
            margin-top: 70px;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(74, 222, 128, 0.1) 0%, transparent 70%);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            animation: float 6s ease-in-out infinite;
            z-index: 0;
        }

        @keyframes float {
            0%, 100% { transform: translate(-50%, -50%); }
            50% { transform: translate(-50%, -100px); }
        }

        .hero-content {
            position: relative;
            z-index: 1;
            max-width: 900px;
            animation: slideInDown 1s ease-out;
        }

        @keyframes slideInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .discord-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(88, 101, 242, 0.1);
            border: 1px solid rgba(88, 101, 242, 0.3);
            padding: 12px 20px;
            border-radius: 20px;
            margin-bottom: 30px;
            font-size: 14px;
            font-weight: 600;
            color: #5865f2;
        }

        h1 {
            font-size: 72px;
            font-weight: 700;
            margin-bottom: 20px;
            line-height: 1.1;
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: slideInDown 1s ease-out 0.1s both;
        }

        .subtitle {
            font-size: 20px;
            color: #a1a1a1;
            margin-bottom: 50px;
            font-weight: 300;
            animation: slideInUp 1s ease-out 0.2s both;
        }

        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .cta-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-bottom: 80px;
            flex-wrap: wrap;
            animation: slideInUp 1s ease-out 0.3s both;
        }

        .btn {
            padding: 16px 44px;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .btn-primary {
            background: linear-gradient(135deg, #5865f2 0%, #4752c4 100%);
            color: #ffffff;
            box-shadow: 0 10px 30px rgba(88, 101, 242, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 50px rgba(88, 101, 242, 0.5);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateY(-3px);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            max-width: 600px;
            margin: 0 auto;
            animation: slideInUp 1s ease-out 0.4s both;
        }

        .stat {
            text-align: center;
            padding: 30px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .stat:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(74, 222, 128, 0.3);
            transform: translateY(-5px);
        }

        .stat-number {
            font-size: 32px;
            font-weight: 700;
            color: #4ade80;
            margin-bottom: 10px;
        }

        .stat-label {
            font-size: 12px;
            color: #a1a1a1;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-weight: 500;
        }

        .features {
            padding: 100px 50px;
            background: rgba(0, 0, 0, 0.3);
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        .section-title {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 60px;
            text-align: center;
            animation: slideInDown 1s ease-out;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .feature-card {
            padding: 40px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .feature-card:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(74, 222, 128, 0.3);
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(74, 222, 128, 0.1);
        }

        .feature-icon {
            font-size: 40px;
            margin-bottom: 20px;
        }

        .feature-title {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 15px;
            color: #4ade80;
        }

        .feature-desc {
            color: #a1a1a1;
            font-size: 14px;
            line-height: 1.8;
        }

        .commands {
            padding: 100px 50px;
            background: rgba(255, 255, 255, 0.02);
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        .commands-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .command-box {
            padding: 20px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            color: #4ade80;
            transition: all 0.3s ease;
        }

        .command-box:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(74, 222, 128, 0.3);
            transform: translateX(5px);
        }

        footer {
            padding: 40px;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(0, 0, 0, 0.5);
        }

        footer p {
            color: #707070;
            font-size: 13px;
        }

        footer a {
            color: #4ade80;
            text-decoration: none;
        }

        @media (max-width: 768px) {
            header { padding: 0 24px; }
            h1 { font-size: 42px; }
            .subtitle { font-size: 16px; }
            .cta-buttons { flex-direction: column; gap: 12px; }
            .btn { width: 100%; justify-content: center; }
            .stats { grid-template-columns: 1fr; gap: 15px; }
            .features, .commands { padding: 60px 24px; }
            .section-title { font-size: 32px; margin-bottom: 40px; }
            .hero { padding: 100px 24px 60px; }
            nav { display: none; }
        }
    </style>
</head>
<body>

<header>
    <div class="logo">Spring</div>
    <nav>
        <a href="/">Home</a>
        <a href="#features">Features</a>
        <a href="#commands">Commands</a>
    </nav>
</header>

<section class="hero">
    <div class="hero-content">
        <div class="discord-badge">
            🤖 Discord Bot
        </div>

        <h1>SpringBot</h1>
        <p class="subtitle">Your AI-powered Discord bot for business assistance, scheduling, and support — available 24/7 in your server.</p>

        <div class="cta-buttons">
            <a href="https://discord.com/oauth2/authorize?client_id=1491090442945560716&permissions=1099514865664&integration_type=0&scope=bot+applications.commands" class="btn btn-primary">
                ➕ Add to Discord
            </a>
            <a href="/" class="btn btn-secondary">
                ← Back Home
            </a>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">50+</div>
                <div class="stat-label">Commands</div>
            </div>
            <div class="stat">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Available</div>
            </div>
            <div class="stat">
                <div class="stat-number">AI</div>
                <div class="stat-label">Powered</div>
            </div>
        </div>
    </div>
</section>

<section class="features" id="features">
    <h2 class="section-title">Features</h2>
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Ultra-Smart AI</div>
            <p class="feature-desc">Engage with remarkably intelligent, empathetic AI that understands context and responds like a wise friend.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🗓️</div>
            <div class="feature-title">Appointments</div>
            <p class="feature-desc">Manage appointments in Discord with automated booking and reminders.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎵</div>
            <div class="feature-title">Music</div>
            <p class="feature-desc">Play SoundCloud tracks in voice channels with queue management and controls.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Economy</div>
            <p class="feature-desc">SpringCoin system with daily rewards and balance checking.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎓</div>
            <div class="feature-title">A+ Study</div>
            <p class="feature-desc">Study CompTIA A+ with flashcards, quizzes, and comprehensive notes.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Moderation</div>
            <p class="feature-desc">Ban, kick, purge messages, and advanced server management tools.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎮</div>
            <div class="feature-title">Fun Commands</div>
            <p class="feature-desc">Roast players, flip coins, roll dice, ask magic 8-ball, and more!</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Customization</div>
            <p class="feature-desc">Custom welcome/goodbye messages and server configuration options.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <div class="feature-title">Spring Integration</div>
            <p class="feature-desc">Full integration with Spring Virtual Office for seamless support.</p>
        </div>
    </div>
</section>

<section class="commands" id="commands">
    <h2 class="section-title">Top Commands</h2>
    <div class="commands-grid">
        <div class="command-box">!spring — Open Spring VO</div>
        <div class="command-box">!springchat — Chat with AI</div>
        <div class="command-box">!play — Play music</div>
        <div class="command-box">!ask — Ask ChatGPT</div>
        <div class="command-box">!balance — Check coins</div>
        <div class="command-box">!daily — Daily reward</div>
        <div class="command-box">!aplusquiz — A+ quiz</div>
        <div class="command-box">!roast — Roast member</div>
        <div class="command-box">!ban — Ban user</div>
        <div class="command-box">!help — All commands</div>
        <div class="command-box">!ping — Check latency</div>
        <div class="command-box">!8ball — Magic 8-ball</div>
    </div>
</section>

<footer>
    <p>SpringBot © 2025 | Part of <a href="/">Spring Virtual Office</a></p>
    <p style="margin-top: 15px; font-size: 12px;">Made with 🌿 by Spring</p>
</footer>

</body>
</html>
    """)


@app.post("/api/chat")
async def api_chat(payload: ChatRequest):
    message = payload.message.strip()

    if not message:
        return {
            "reply": "I'm all ears—what's on your mind?"
        }

    # Check for crisis
    if detect_crisis(message):
        return {
            "reply": "❤️ I'm genuinely concerned about what you just shared. If you're having thoughts of self-harm or hurting others, please reach out to 988 - the Suicide & Crisis Lifeline. It's available 24/7, completely confidential, and staffed by people who care. You matter, and you deserve real support right now."
        }

    # Check for sadness
    if detect_sadness(message):
        return {
            "reply": "💙 I hear you, and I can sense something difficult is weighing on you right now. What you're feeling is valid. If you'd like professional support from a licensed therapist, BetterHelp has compassionate people available 24/7 at https://www.betterhelp.com/get-started/. You don't have to go through this alone."
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

        # Send email and SMS
        email_sent = send_email(name, email, phone, message)
        sms_sent = send_sms(name, email, phone, message)

        if email_sent or sms_sent:
            return {
                "success": True,
                "message": "Ticket submitted successfully!",
                "ticket_id": f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
        else:
            return {
                "success": False,
                "error": "Failed to send notifications"
            }, 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }, 500

@app.get("/health")
async def health():
    return {
        "status": "online"
    }
