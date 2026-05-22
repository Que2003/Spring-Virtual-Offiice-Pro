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

/* ==================== ANIMATED BACKGROUND ==================== */

.bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000000;
  z-index: -1;
}

/* ==================== SPRINGBOT ANIMATION ==================== */

.springbot-container {
  position: fixed;
  bottom: 40px;
  right: 40px;
  z-index: 500;
}

.springbot {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%);
  border-radius: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  animation: float 3s ease-in-out infinite;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.springbot:hover {
  transform: translateY(-10px);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.springbot-emoji {
  font-size: 48px;
  animation: bounce 1s ease-in-out infinite;
}

.springbot-text {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.pulse-ring {
  position: absolute;
  width: 140px;
  height: 140px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 30px;
  animation: pulse 2s ease-out infinite;
  pointer-events: none;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}

/* ==================== HEADER ==================== */

header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
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
  top: 50px;
  right: 0;
  background: rgba(30, 30, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  min-width: 150px;
  max-height: 300px;
  overflow-y: auto;
  backdrop-filter: blur(20px);
  display: none;
  z-index: 2000;
}

.theme-menu.active {
  display: block;
}

.theme-option {
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
  font-weight: 500;
  border-left: 2px solid transparent;
}

.theme-option:hover {
  background: rgba(255, 255, 255, 0.08);
}

.theme-option.active {
  background: rgba(255, 255, 255, 0.12);
  border-left-color: #ffffff;
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
  padding-top: 60px;
  text-align: center;
}

.content {
  max-width: 800px;
  padding: 0 40px;
  animation: fadeIn 1s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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

.subtitle {
  font-size: 18px;
  color: #a1a1a1;
  margin-bottom: 50px;
  font-weight: 300;
  animation: slideInUp 1s ease-out 0.2s both;
  letter-spacing: 0.3px;
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.cta-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 100px;
  animation: slideInUp 1s ease-out 0.3s both;
  flex-wrap: wrap;
}

.btn {
  padding: 14px 40px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 13px;
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
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(255, 255, 255, 0.15);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: #f5f7fa;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-2px);
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
  .subtitle { font-size: 16px; margin-bottom: 40px; }
  header { padding: 0 24px; }
  .cta-buttons { gap: 12px; margin-bottom: 60px; }
  .btn { padding: 12px 28px; font-size: 12px; }
  .stats { grid-template-columns: 1fr; gap: 24px; }
  .springbot-container { bottom: 24px; right: 24px; }
  .springbot { width: 100px; height: 100px; }
  .springbot-emoji { font-size: 40px; }
}

</style>
</head>
<body>

<div class="bg"></div>

<header>
  <div class="logo">Spring</div>
  <div style="position: relative;">
    <button class="theme-btn" onclick="toggleThemeMenu()">Themes</button>
    <div class="theme-menu" id="themeMenu">
      <div class="theme-option active" onclick="switchTheme('dark')">Dark</div>
      <div class="theme-option" onclick="switchTheme('light')">Light</div>
    </div>
  </div>
</header>

<main>
  <div class="content">
    <h1>Spring Virtual Office</h1>
    <p class="subtitle">The intelligent workspace for modern teams</p>
    
    <div class="cta-buttons">
      <button class="btn btn-primary" onclick="window.location.href='/chat'">Start Now</button>
      <button class="btn btn-secondary" onclick="alert('Coming soon!')">Learn More</button>
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

<div class="springbot-container" onclick="window.location.href='/chat'">
  <div class="pulse-ring"></div>
  <div class="springbot">
    <div class="springbot-emoji">🌿</div>
    <div class="springbot-text">SpringBot</div>
  </div>
</div>

<script>

function toggleThemeMenu() {
  const menu = document.getElementById('themeMenu');
  menu.classList.toggle('active');
}

function switchTheme(theme) {
  if (theme === 'light') {
    document.body.style.background = '#ffffff';
    document.body.style.color = '#000000';
    document.querySelector('header').style.background = 'rgba(255, 255, 255, 0.5)';
    document.querySelector('header').style.borderBottomColor = 'rgba(0, 0, 0, 0.08)';
    document.querySelector('.subtitle').style.color = '#656565';
    document.querySelector('.stat-label').style.color = '#929292';
  } else {
    document.body.style.background = '#000000';
    document.body.style.color = '#ffffff';
    document.querySelector('header').style.background = 'rgba(0, 0, 0, 0.5)';
    document.querySelector('header').style.borderBottomColor = 'rgba(255, 255, 255, 0.08)';
    document.querySelector('.subtitle').style.color = '#a1a1a1';
    Array.from(document.querySelectorAll('.stat-label')).forEach(el => el.style.color = '#707070');
  }
  
  localStorage.setItem('springTheme', theme);
  
  const options = document.querySelectorAll('.theme-option');
  options.forEach(opt => opt.classList.remove('active'));
  event.target.classList.add('active');
  
  document.getElementById('themeMenu').classList.remove('active');
}

// Load saved theme
window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('springTheme') || 'dark';
  switchTheme(savedTheme);
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
            "reply": "❤️ I'm concerned about what you're saying. If you're having thoughts of self-harm or harming others, please call 988 - the Suicide & Crisis Lifeline. It's available 24/7 and completely confidential. You deserve professional support."
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
