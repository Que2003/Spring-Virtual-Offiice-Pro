from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os
import anthropic
from dotenv import load_dotenv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

router = APIRouter()

# --- Config ---
YOUR_EMAIL = "dillingsq2003@gmail.com"
YOUR_PHONE = "281-763-9753"
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE = os.getenv("RECIPIENT_PHONE")

# Anthropic client
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# --- Models ---
class TicketRequest(BaseModel):
    name: str
    email: str
    phone: str = ""
    message: str


class ChatRequest(BaseModel):
    message: str
    history: list = []


# --- Helpers ---
def send_email_notification(name, email, phone, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = YOUR_EMAIL
        msg["Subject"] = f"New Ticket Submitted - {name}"
        body = f"""A new ticket has been submitted:

Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}
Message:
{message}

Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        msg.attach(MIMEText(body, "plain"))

        confirmation = MIMEMultipart()
        confirmation["From"] = SMTP_USER
        confirmation["To"] = email
        confirmation["Subject"] = "We Received Your Ticket - Spring Virtual Office"
        conf_body = f"""Hello {name},

Thank you for contacting Spring Virtual Office! We've received your ticket and will review it shortly.

Ticket Details:
{message}

We'll get back to you within 24 hours.

Best regards,
Spring Virtual Office Team"""
        confirmation.attach(MIMEText(conf_body, "plain"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            server.send_message(confirmation)

        return True, "Email sent successfully"
    except Exception as e:
        print(f"Email error: {e}")
        return False, str(e)


def send_sms_notification(name, email, phone, message):
    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        sms_body = f"New ticket from {name}:\nEmail: {email}\nPhone: {phone or 'N/A'}\nMessage: {message[:100]}..."
        client.messages.create(body=sms_body, from_=TWILIO_PHONE_NUMBER, to=RECIPIENT_PHONE)
        return True, "SMS sent"
    except Exception as e:
        print(f"SMS error: {e}")
        return False, str(e)


# --- Routes ---
@router.post("/api/submit-ticket")
async def submit_ticket(data: TicketRequest):
    name = data.name.strip()
    email = data.email.strip()
    phone = data.phone.strip()
    message = data.message.strip()

    if not name or not email or not message:
        return JSONResponse({"success": False, "error": "Missing required fields"}, status_code=400)
    if "@" not in email or "." not in email:
        return JSONResponse({"success": False, "error": "Invalid email address"}, status_code=400)

    email_success, _ = send_email_notification(name, email, phone, message)
    sms_success, _ = send_sms_notification(name, email, phone, message)

    if email_success or sms_success:
        return JSONResponse({
            "success": True,
            "message": "Ticket submitted successfully!",
            "ticket_id": f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        })
    return JSONResponse({"success": False, "error": "Failed to send notification"}, status_code=500)


@router.post("/api/chat")
async def chat_api(data: ChatRequest):
    try:
        messages = data.history + [{"role": "user", "content": data.message}]
        response = claude.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=(
                "You are Spring, a warm and professional AI front desk assistant for Spring Virtual Office. "
                "You greet visitors, answer questions about services, help book appointments by collecting "
                "their name, email, and preferred time, and detect when someone is distressed and respond "
                "with care. Be concise, friendly, and helpful."
            ),
            messages=messages,
        )
        reply = response.content[0].text
        return JSONResponse({"success": True, "reply": reply})
    except Exception as e:
        print(f"Claude error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@router.get("/chat")
async def chat_page():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Spring AI Chat</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:linear-gradient(135deg,#f8fbff,#dff5ff,#eef7ff);
  min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;
}
.chat-container{
  width:100%;max-width:680px;height:90vh;max-height:780px;
  background:rgba(255,255,255,.75);backdrop-filter:blur(30px);
  border:1px solid rgba(255,255,255,.9);border-radius:36px;
  box-shadow:0 40px 100px rgba(57,120,255,.15);
  display:flex;flex-direction:column;overflow:hidden;
}
.chat-header{
  padding:24px 28px;border-bottom:1px solid rgba(0,0,0,.06);
  font-weight:800;font-size:18px;display:flex;align-items:center;gap:10px;
}
.status{width:10px;height:10px;border-radius:50%;background:#3de88a;}
.messages{flex:1;overflow-y:auto;padding:24px 28px;display:flex;flex-direction:column;gap:14px;}
.bubble{
  padding:14px 18px;border-radius:20px;max-width:80%;line-height:1.6;font-size:15px;
}
.ai{background:white;box-shadow:0 4px 20px rgba(0,0,0,.07);align-self:flex-start;}
.user{background:#3978ff;color:white;align-self:flex-end;}
.chat-input{
  padding:18px 24px;border-top:1px solid rgba(0,0,0,.06);
  display:flex;gap:12px;align-items:center;
}
input{
  flex:1;padding:14px 18px;border-radius:18px;border:1.5px solid #e0eaff;
  font-size:15px;outline:none;background:white;
}
input:focus{border-color:#3978ff;}
button{
  padding:14px 22px;border-radius:18px;border:none;
  background:#3978ff;color:white;font-weight:700;cursor:pointer;font-size:15px;
}
button:disabled{opacity:.5;cursor:not-allowed;}
.typing{color:#8899aa;font-size:14px;padding:4px 8px;}
a.back{display:block;margin-top:16px;color:#3978ff;text-decoration:none;font-weight:600;font-size:14px;}
</style>
</head>
<body>
<div class="chat-container">
  <div class="chat-header">
    <span>🌿</span> Spring AI
    <div class="status"></div>
  </div>
  <div class="messages" id="messages">
    <div class="bubble ai">Hello! I'm Spring, your virtual front desk assistant. I can answer questions, help book an appointment, or connect you with our team. What brings you here today?</div>
  </div>
  <div class="chat-input">
    <input id="input" type="text" placeholder="Type a message..." onkeydown="if(event.key==='Enter')sendMessage()">
    <button id="sendBtn" onclick="sendMessage()">Send</button>
  </div>
</div>
<a class="back" href="/">← Back to home</a>

<script>
const history = [];

async function sendMessage() {
  const input = document.getElementById('input');
  const text = input.value.trim();
  if (!text) return;

  addBubble(text, 'user');
  history.push({ role: 'user', content: text });
  input.value = '';
  setLoading(true);

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, history: history.slice(0, -1) })
    });
    const data = await res.json();
    const reply = data.reply || 'Sorry, something went wrong.';
    addBubble(reply, 'ai');
    history.push({ role: 'assistant', content: reply });
  } catch (e) {
    addBubble('Sorry, I could not connect. Please try again.', 'ai');
  }
  setLoading(false);
}

function addBubble(text, type) {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = `bubble ${type}`;
  div.textContent = text;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function setLoading(on) {
  document.getElementById('sendBtn').disabled = on;
}
</script>
</body>
</html>
""")
