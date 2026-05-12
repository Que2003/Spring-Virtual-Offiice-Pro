# Railway Setup — Super Simple Version

## 🚀 The Absolute Minimum You Need to Know

### Step 1: Push Your Code to GitHub
```bash
git init
git add .
git commit -m "Spring Virtual Office"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/spring-virtual-office.git
git push -u origin main
```

### Step 2: Go to Railway
Visit: https://railway.app

### Step 3: Login with GitHub
Click "Login with GitHub"

### Step 3: Create Project
Click "New Project" or "+ Create"

### Step 4: Deploy Your Repo
Select "Deploy from GitHub"
Select "spring-virtual-office"
Click "Deploy"

**WAIT a few minutes while it builds...**

### Step 5: Add 2 Services

#### Service 1: Website
- Name it: `website` or `web`
- Language: **Python**
- Start command: 
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Service 2: Bot
- Name it: `bot` or `discord-bot`
- Language: **Python**
- Start command:
```
python run_discord_bot.py
```

### Step 6: Add Your Keys
In Railway project settings, add variables:

```
OPENAI_API_KEY=sk-your-key-here
DISCORD_TOKEN=MTA-your-token-here
OWNER_DISCORD_ID=your-discord-id
OWNER_EMAIL=your@email.com
BUSINESS_NAME=Spring Virtual Office
ADMIN_SECRET=your-strong-password
DB_PATH=spring_office.db
```

### Done! ✅

Both services will start automatically.

Your website URL appears in the Railway dashboard.
Your bot comes online automatically.

---

## When Railway Asks You...

| Railway Asks | You Answer |
|--------------|-----------|
| What platform? | **Python** |
| Which repo? | **spring-virtual-office** |
| What's the start command? | **See above** |
| Need a database? | **No** (SQLite is built-in) |
| Need Docker? | **No** (Railway does it) |

---

## That's Actually It

Seriously. That's the whole process:

1. Push code
2. Login to Railway
3. Deploy repo
4. Add 2 services (website + bot)
5. Add environment variables
6. Click deploy

**5 minutes later: You're live! 🎉**

---

## The URLs You'll Get

**Website:**
```
https://spring-virtual-office-prod.up.railway.app
```

**Bot:**
```
Automatically online in your Discord server
```

**Admin:**
```
https://spring-virtual-office-prod.up.railway.app/admin
```

---

## What to Do Next

1. Visit your website URL
2. Test `/chat` command
3. Test `/book` command
4. Test admin at `/admin`
5. Share the URL with your friends
6. Celebrate! 🎉

---

## Common Railway Terms Explained

| Term | What It Means |
|------|---------------|
| **Service** | A thing that runs (website = service, bot = service) |
| **Environment** | Your secret keys/variables |
| **Port** | Where your app listens (Railway handles this) |
| **Deployment** | When Railway runs your code |
| **Status** | Green = running, Yellow = building, Red = error |
| **Logs** | Text that shows what's happening |
| **Variables** | Your secret API keys |

---

## If Something Goes Wrong

**Website won't load?**
- Check the logs (click service → view logs)
- Check environment variables are set
- Restart the service

**Bot won't come online?**
- Check logs (click bot service → view logs)
- Check DISCORD_TOKEN is correct
- Make sure bot is in your Discord server

**Variables not working?**
- Redeploy (Railway auto-redeploys when vars change)
- Check spellings exactly match

---

## Remember

✅ Language = Python
✅ Website command = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
✅ Bot command = `python run_discord_bot.py`
✅ Variables = Your API keys
✅ Done!

That's literally everything you need to know.

**No Docker. No complexity. Just Python. Simple.** 🚀
