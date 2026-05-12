# Railway Service Selection Guide

## 🎯 What to Choose on Railway

When you create a project on Railway, you need to specify what to run. Here's what to pick:

---

## For Your Spring Virtual Office

You need **2 services**:

### Service 1: Website (FastAPI)
**What to select:** `Python`
**What to run:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**In Railway dashboard:**
1. Click "New" → "Database" (or skip this, you don't need it for SQLite)
2. Click "New" → "Service"
3. Select "GitHub repo"
4. Select your `spring-virtual-office` repo
5. Railway auto-detects Python ✅

**Configuration:**
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Port:** 8000 (Railway sets this automatically)
- **Environment:** Add your .env variables

### Service 2: Discord Bot
**What to select:** `Python`
**What to run:** `python run_discord_bot.py`

**In Railway dashboard:**
1. Click "New" → "Service" (in same project)
2. Select "GitHub repo"
3. Select your `spring-virtual-office` repo again
4. Railway auto-detects Python ✅

**Configuration:**
- **Start command:** `python run_discord_bot.py`
- **Environment:** Same variables as website
- **Keep running:** Yes (set to run always, not on schedule)

---

## Simple Version

### Railway will ask you:

**Question 1: What platform?**
Answer: **Python**

**Question 2: Which repo?**
Answer: **spring-virtual-office**

**Question 3: What to run?**

For Website Service:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

For Bot Service:
```
python run_discord_bot.py
```

---

## Step-by-Step on Railway

### Create Website Service:

1. Go to https://railway.app
2. Log in with GitHub
3. Click "+ New Project"
4. Click "Deploy from GitHub repo"
5. Select your `spring-virtual-office` repo
6. Click "Deploy"
7. Wait for auto-detection
8. Railway shows: `Detected: Python 3.x`
9. Click "Configure"
10. Set **Start Command** to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
11. Save ✅

### Create Bot Service:

1. In same Railway project, click "+ New"
2. Click "Service"
3. Click "GitHub"
4. Select `spring-virtual-office` repo again
5. Wait for auto-detection
6. Set **Start Command** to: `python run_discord_bot.py`
7. Save ✅

### Add Environment Variables to Both:

1. In Railway dashboard, click "Variables" (applies to whole project)
2. Add all your variables:
```
OPENAI_API_KEY=sk-...
DISCORD_TOKEN=MTA-...
OWNER_DISCORD_ID=123456789
OWNER_EMAIL=your@email.com
BUSINESS_NAME=Spring Virtual Office
ADMIN_SECRET=strong-password
DB_PATH=spring_office.db
```
3. Save → Both services redeploy automatically ✅

---

## What Railway Auto-Detects

Railway is smart! When you connect your GitHub repo, it automatically:

✅ Detects Python
✅ Reads `requirements.txt`
✅ Installs all dependencies
✅ Creates a web service

You just need to tell it:
- **What command to run** (uvicorn for website, python for bot)
- **What environment variables to use** (your .env)

---

## Don't Choose

❌ Docker (Railway handles this for you)
❌ Node.js (you're using Python)
❌ Static (you need to run code)
❌ Database as service (SQLite is built-in)

---

## Visual Flow

```
You push to GitHub
        ↓
Railway detects Python
        ↓
Railway installs requirements
        ↓
You tell Railway what command to run
        ↓
Website: uvicorn app.main:app
Bot: python run_discord_bot.py
        ↓
Railway runs both simultaneously
        ↓
Your website is live!
Your bot is online!
✅ Done!
```

---

## Real Example

### For your Spring Virtual Office:

**Service #1: Web**
- Language: Python
- Repo: spring-virtual-office
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Port: 8000 (auto)
- URL: `https://spring-virtual-office-prod.up.railway.app` ✅

**Service #2: Bot**
- Language: Python
- Repo: spring-virtual-office
- Start: `python run_discord_bot.py`
- No port needed (Discord API handles it)
- Status: Online ✅ (shows in your Discord server)

---

## Environment Variables on Railway

When Railway asks for variables, paste these:

```
OPENAI_API_KEY=sk-proj-abc123xyz...
DISCORD_TOKEN=MTA5NDU2ODQwOTY0NzQ2MzExMg.GabcDe.xyz123...
OWNER_DISCORD_ID=123456789
OWNER_EMAIL=your@example.com
BUSINESS_NAME=Spring Virtual Office
ADMIN_SECRET=MyStrongPassword123!@#
DB_PATH=spring_office.db
```

Get these from:
- **OPENAI_API_KEY:** https://openai.com/account/api-keys
- **DISCORD_TOKEN:** https://discord.com/developers/applications (Bot section)
- **OWNER_DISCORD_ID:** Right-click your Discord username (Developer Mode on)
- Rest: You create yourself

---

## That's It!

Railway handles:
- Installing Python
- Installing packages from requirements.txt
- Running your code
- Keeping it online 24/7
- SSL/HTTPS automatically
- Database persistence
- Logs and monitoring

You just provide:
- Your GitHub repo
- Start command
- Environment variables

**Everything else is automatic!** ✅

---

## Checklist for Railway

- [ ] GitHub repo pushed
- [ ] Railway account created (login with GitHub)
- [ ] Project created
- [ ] Website service added with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Bot service added with `python run_discord_bot.py`
- [ ] Environment variables added to project
- [ ] Website service deploying (green status)
- [ ] Bot service deploying (green status)
- [ ] Website URL live (check deployment)
- [ ] Bot online in Discord
- [ ] Test `/chat hello`
- [ ] Test `/book`
- [ ] Test admin panel
- [ ] Celebrate! 🎉

---

## Common Questions

**Q: Do I need to pick "Docker"?**
A: No! Railway handles containerization automatically. Just pick Python.

**Q: Do I need a database service?**
A: No! SQLite is local to your app. Railway includes it automatically.

**Q: Can I run both website and bot?**
A: Yes! Create 2 Python services with different start commands.

**Q: What if Railway fails to detect Python?**
A: Make sure you have `requirements.txt` in the root folder.

**Q: How do I update my code?**
A: Just push to GitHub! Railway auto-redeploys.

**Q: What's the $PORT variable?**
A: Railway assigns a port dynamically. $PORT gets that value automatically.

**Q: How do I see logs?**
A: Click "Deployments" → Click your service → View logs.

**Q: Can I add a custom domain?**
A: Yes! Railway Settings → Add domain → Update DNS.

---

## Final Answer

### On Railway, for Spring Virtual Office, you need:

1. **Python service #1 (Website)**
   - Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Python service #2 (Bot)**
   - Command: `python run_discord_bot.py`

3. **Environment variables** (shared by both)
   - Your OpenAI key, Discord token, etc.

**Railway auto-handles everything else!**

That's literally it. 🚀
