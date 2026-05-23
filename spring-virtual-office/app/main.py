from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.chatbot_routes import router as chatbot_router

app = FastAPI()

# Include chatbot routes (ticket submission, /chat page, etc.)
app.include_router(chatbot_router)


@app.get("/")
async def home():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Spring Virtual Office</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:linear-gradient(135deg,#f8fbff,#dff5ff,#eef7ff);
  color:#102033;
  min-height:100vh;
}
header{
  display:flex;justify-content:space-between;align-items:center;
  padding:24px 7%;
}
.logo{font-size:24px;font-weight:800}
nav a{margin-left:24px;color:#102033;text-decoration:none;font-weight:600}
.hero{
  display:grid;grid-template-columns:1.1fr .9fr;gap:50px;
  align-items:center;padding:70px 7%;
}
.badge{
  display:inline-block;padding:10px 16px;border-radius:999px;
  background:rgba(255,255,255,.7);backdrop-filter:blur(20px);
  box-shadow:0 8px 30px rgba(0,0,0,.08);
  margin-bottom:24px;font-weight:700;color:#3978ff;
}
h1{font-size:72px;line-height:1;letter-spacing:-3px;margin-bottom:24px}
p{font-size:20px;color:#4c6075;line-height:1.7}
.buttons{margin-top:34px;display:flex;gap:16px}
button,.btn{
  border:none;border-radius:18px;padding:16px 28px;
  font-weight:800;cursor:pointer;text-decoration:none;
}
.primary{background:#111;color:white}
.secondary{background:white;color:#111;box-shadow:0 10px 30px rgba(0,0,0,.08)}
.demo{
  background:rgba(255,255,255,.65);
  border:1px solid rgba(255,255,255,.8);
  border-radius:36px;padding:28px;
  box-shadow:0 30px 80px rgba(49,118,255,.18);
  backdrop-filter:blur(25px);
}
.chatTop{font-weight:800;margin-bottom:20px}
.bubble{
  padding:14px 18px;border-radius:20px;margin:12px 0;
  max-width:85%;line-height:1.5;
}
.ai{background:white}
.user{background:#3978ff;color:white;margin-left:auto}
section{padding:70px 7%}
.sectionTitle{font-size:44px;margin-bottom:30px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.card{
  background:rgba(255,255,255,.7);
  border:1px solid rgba(255,255,255,.9);
  border-radius:28px;padding:28px;
  box-shadow:0 20px 50px rgba(0,0,0,.07);
}
.card h3{font-size:22px;margin-bottom:12px}
.card p{font-size:16px}
.floating{
  position:fixed;right:26px;bottom:26px;
  width:76px;height:76px;border-radius:26px;
  background:linear-gradient(135deg,#6ee7ff,#3978ff);
  display:flex;align-items:center;justify-content:center;
  color:white;font-size:34px;box-shadow:0 20px 50px rgba(57,120,255,.35);
  cursor:pointer;animation:float 3s ease-in-out infinite;
}
@keyframes float{50%{transform:translateY(-12px)}}
footer{text-align:center;padding:40px;color:#5d6d80}
@media(max-width:850px){
  .hero{grid-template-columns:1fr;padding-top:35px}
  h1{font-size:48px}
  .grid{grid-template-columns:1fr}
  nav{display:none}
}
</style>
</head>
<body>
<header>
  <div class="logo">Spring Virtual Office</div>
  <nav>
    <a href="#features">Features</a>
    <a href="#themes">Themes</a>
    <a href="#how">How it works</a>
  </nav>
</header>

<main class="hero">
  <div>
    <div class="badge">24/7 AI · Response in under 1 second</div>
    <h1>Your business is always open.</h1>
    <p>Spring is an AI front desk that greets visitors, answers questions, books appointments, and detects when someone needs real human care.</p>
    <div class="buttons">
      <a class="btn primary" href="/chat">Try the live demo</a>
      <a class="btn secondary" href="#features">Explore features</a>
    </div>
  </div>

  <div class="demo">
    <div class="chatTop">🌿 Spring AI</div>
    <div class="bubble ai">Hello — I'm Spring. I can answer questions or help book an appointment. What brings you here?</div>
    <div class="bubble user">I'd like to book a consult next Tuesday.</div>
    <div class="bubble ai">Absolutely. What time works best for you, and what's your name?</div>
  </div>
</main>

<section id="features">
  <h2 class="sectionTitle">A front desk that never sleeps.</h2>
  <div class="grid">
    <div class="card"><h3>Intelligent AI Chat</h3><p>Understands context, follow-ups, tone, and real customer intent.</p></div>
    <div class="card"><h3>Appointment Booking</h3><p>Collects name, email, preferred time, and sends appointment details.</p></div>
    <div class="card"><h3>Empathy Detection</h3><p>Recognizes distress, responds carefully, and escalates when needed.</p></div>
    <div class="card"><h3>Multi-Platform</h3><p>Works across your website, Discord, and future business tools.</p></div>
    <div class="card"><h3>Custom Themes</h3><p>Apple minimal, Frutiger Aero, glassmorphism, and business styles.</p></div>
    <div class="card"><h3>24/7 Availability</h3><p>Your business keeps answering even when you are offline.</p></div>
  </div>
</section>

<section id="how">
  <h2 class="sectionTitle">Live in three steps.</h2>
  <div class="grid">
    <div class="card"><h3>01 Connect</h3><p>Tell Spring about your business, services, hours, and goals.</p></div>
    <div class="card"><h3>02 Choose a Voice</h3><p>Pick the personality and design style that matches your brand.</p></div>
    <div class="card"><h3>03 Go Live</h3><p>Add it to your website and let Spring start helping customers.</p></div>
  </div>
</section>

<footer>© 2026 Spring Virtual Office · AI front desk for any business</footer>

<div class="floating" onclick="window.location.href='/chat'">🌿</div>
</body>
</html>
""")
