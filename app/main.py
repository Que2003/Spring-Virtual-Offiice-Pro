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

</style>

</head>

<body>

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

<button
  class="clear"
  onclick="clearChat()"
>
Clear
</button>

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
