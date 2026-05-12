# Spring Virtual Office — Full Implementation Guide

A complete, production-ready AI-powered virtual office platform with **Discord bot**, **website**, and **admin panel**.

## ✨ Features

### Website
- **Homepage** — Beautiful landing page with features, how it works, and CTA
- **Chat Page** — Real-time AI conversation with sidebar quick prompts
- **Appointments** — Multi-step booking form with date/time selection
- **Admin Panel** — Dashboard to view and manage all appointments

### Discord Bot
- **Slash Commands** — `/chat`, `/book`, `/appointments`, `/clear`, `/help`
- **DM Chat** — AI responds to direct messages
- **Appointment Flow** — Multi-step booking directly in Discord
- **Owner Alerts** — Instant DM notifications for new appointments, empathy triggers, and crisis detection
- **Conversation Memory** — Maintains context across messages per user

### AI & Safety
- **GPT-4 Integration** — Intelligent, context-aware responses
- **Empathy Detection** — Automatically alerts you when users are stressed
- **Crisis Detection** — Identifies crisis language and responds with 988 lifeline info
- **Database Storage** — Tracks all conversations and appointments

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo>
cd spring-virtual-office
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with:
```
OPENAI_API_KEY=sk-...
DISCORD_TOKEN=MTA0...
OWNER_DISCORD_ID=123456789
OWNER_EMAIL=you@example.com
BUSINESS_NAME=Spring Virtual Office
ADMIN_SECRET=spring-admin-2025
```

### 3. Run Both Web & Bot

**Option A: Run Web Server Only**
```bash
uvicorn app.main:app --reload
```
Open http://localhost:8000

**Option B: Run Discord Bot Only**
```bash
python run_discord_bot.py
```

**Option C: Run Both Together** (recommended for development)

Terminal 1:
```bash
uvicorn app.main:app --reload --port 8000
```

Terminal 2:
```bash
python run_discord_bot.py
```

---

## 📁 Project Structure

```
spring-virtual-office/
├── app/
│   ├── main.py                    # FastAPI backend
│   ├── discord_bot/
│   │   └── bot.py                # Discord bot (full implementation)
│   └── static/
│       ├── index.html            # Homepage
│       ├── chat.html             # Chat page
│       ├── appointments.html     # Booking form
│       └── admin.html            # Admin panel
├── run_discord_bot.py            # Bot entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md                      # This file
```

---

## 🌐 Website Routes

| Route | Purpose |
|-------|---------|
| `/` | Homepage & landing page |
| `/chat` | AI chat interface |
| `/appointments` | Appointment booking form |
| `/admin` | Admin dashboard (password protected) |

### Admin Panel
- **URL:** `http://localhost:8000/admin`
- **Secret:** Whatever you set in `ADMIN_SECRET` env var (default: `spring-admin-2025`)
- **Features:**
  - View all appointments
  - Filter by status (pending, confirmed, completed, cancelled)
  - Change appointment status with one click
  - Copy client emails

---

## 🤖 Discord Bot Setup

### Get Your Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application → "Spring Virtual Office"
3. Go to "Bot" → "Add Bot"
4. Copy the token → paste into `.env` as `DISCORD_TOKEN`
5. Enable "Message Content Intent" under Privileged Gateway Intents

### Get Your User ID
1. Enable Developer Mode in Discord (Settings → Advanced → Developer Mode)
2. Right-click your username → "Copy User ID"
3. Paste into `.env` as `OWNER_DISCORD_ID`

### Invite Bot to Server
1. Go to OAuth2 → URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select permissions: `Send Messages`, `Read Messages`, `Slash Commands`
4. Copy generated URL → paste in browser to invite

### Bot Commands

**User Commands:**
- `/chat [message]` — Chat with the AI
- `/book` — Start appointment booking flow
- `/clear` — Clear your conversation history
- `/help` — Show all commands

**Admin Commands:**
- `/appointments` — View all pending appointments

**DM Features:**
- Send any message in DMs → AI responds
- Crisis language detected automatically
- Empathy triggers alert owner

---

## 🔌 API Endpoints

### POST `/api/chat`
Request:
```json
{ "session_id": "sess_123", "message": "Hello!" }
```
Response:
```json
{ "reply": "Hi there! How can I help?", "is_crisis": false }
```

### POST `/api/appointments`
Request:
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "preferred_time": "Tuesday at 2pm",
  "reason": "Consultation"
}
```
Response:
```json
{ "success": true, "id": 1, "message": "Appointment request received!" }
```

### GET `/api/appointments?secret=your_secret`
Returns all appointments (requires admin secret)

### PATCH `/api/appointments/{id}?secret=your_secret`
Update appointment status:
```json
{ "status": "confirmed" }
```

### GET `/api/health`
Health check endpoint

---

## 🚀 Deployment

### Railway.app (Recommended)
1. Push code to GitHub
2. Create new Railway project
3. Connect your GitHub repo
4. Add environment variables
5. Deploy!

Your app will be live at `https://your-app.railway.app`

### Environment Variables for Production
```
OPENAI_API_KEY
DISCORD_TOKEN
OWNER_DISCORD_ID
OWNER_EMAIL
BUSINESS_NAME
ADMIN_SECRET
DATABASE_URL (if using cloud DB)
```

---

## 💾 Database

Uses SQLite locally (`spring_office.db`). Tables:
- **appointments** — All appointment requests with status
- **conversations** — Chat history (web sessions)
- **web_conversations** — Web-based chat history

For production, consider:
- PostgreSQL via Railway
- MongoDB via MongoDB Atlas
- Cloud SQL

---

## 🔐 Safety Features

✅ **Crisis Detection**
- Automatically detects crisis language (suicide, self-harm, etc.)
- Responds with 988 Lifeline information
- Alerts owner immediately

✅ **Empathy Detection**
- Identifies when users are stressed/overwhelmed
- Sends alert to owner for follow-up

✅ **Admin Authentication**
- Admin panel requires secret key
- No appointments exposed without authentication

✅ **CORS Enabled**
- Cross-origin requests allowed for integration

---

## 🎨 Customization

### Change Colors
Edit CSS variables in HTML files:
```css
:root {
  --sage: #7a9e7e;        /* Primary color */
  --gold: #c4a85a;        /* Accent color */
  --charcoal: #1e2220;    /* Dark color */
  /* ... more vars */
}
```

### Change Fonts
Update Google Fonts import in HTML `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=YOUR_FONT&display=swap" rel="stylesheet" />
```

### Update AI System Prompt
Edit `SYSTEM_PROMPT` in:
- `app/main.py` (website)
- `app/discord_bot/bot.py` (Discord)

### Change Crisis/Empathy Keywords
Edit keyword lists in both files:
```python
CRISIS_KEYWORDS = ["suicide", "kill myself", ...]
EMPATHY_KEYWORDS = ["stressed", "overwhelmed", ...]
```

---

## 🐛 Troubleshooting

### Bot Not Responding
- Check `DISCORD_TOKEN` is correct
- Verify bot has "Message Content Intent" enabled
- Ensure bot is invited to server with correct permissions
- Check logs: `python run_discord_bot.py`

### Chat Not Working
- Verify `OPENAI_API_KEY` is valid
- Check network connection
- Clear browser cache
- Try incognito window

### Admin Panel Not Loading
- Verify correct `ADMIN_SECRET`
- Check browser console for errors
- Ensure database file exists

### Appointments Not Saving
- Check `DB_PATH` is writable
- Verify database hasn't been deleted
- Restart the server

---

## 📞 Support

For issues:
1. Check logs: `python run_discord_bot.py` or browser console
2. Verify all environment variables are set
3. Ensure OpenAI API key is valid (test at openai.com)
4. Test database: SQLite should auto-create tables on first run

---

## 📄 License

This project is yours to deploy, customize, and use commercially.

---

## 🌟 Next Steps

1. ✅ Set up environment variables
2. ✅ Test locally (both web and bot)
3. ✅ Customize branding and colors
4. ✅ Deploy to Railway
5. ✅ Add bot to your Discord server
6. ✅ Share website URL with clients
7. ✅ Monitor admin panel for appointments

---

**Spring Virtual Office — Always available for your clients. 🌿**
