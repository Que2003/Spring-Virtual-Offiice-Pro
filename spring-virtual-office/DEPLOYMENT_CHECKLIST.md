# 🚀 Spring Virtual Office — Launch Checklist

## Pre-Launch Checklist

### ✅ Project Setup (10 min)
- [ ] Download all files from outputs folder
- [ ] Create folder structure: `app/`, `app/static/`, `app/discord_bot/`
- [ ] Copy files into correct locations
- [ ] Copy `.env.example` → `.env`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`

### ✅ Environment Setup (15 min)
- [ ] Get OpenAI API key from [openai.com/account/api-keys](https://openai.com/account/api-keys)
- [ ] Create Discord application: [discord.com/developers](https://discord.com/developers)
- [ ] Get Discord bot token (copy to clipboard)
- [ ] Get your Discord user ID (right-click username, copy)
- [ ] Fill in `.env`:
  ```
  OPENAI_API_KEY=sk-...
  DISCORD_TOKEN=MTA...
  OWNER_DISCORD_ID=123456789
  OWNER_EMAIL=you@example.com
  BUSINESS_NAME=Your Business
  ADMIN_SECRET=choose-a-strong-password
  ```
- [ ] Save `.env` (DO NOT COMMIT)

### ✅ Local Testing (30 min)

#### Website Testing
- [ ] Start web server: `uvicorn app.main:app --reload`
- [ ] Open http://localhost:8000
- [ ] Test Homepage
  - [ ] Loads without errors
  - [ ] All sections visible (hero, features, stats, CTA)
  - [ ] Links work (Chat, Appointments)
  - [ ] Animations play smoothly
- [ ] Test Chat Page
  - [ ] Page loads
  - [ ] Can type messages
  - [ ] Send button works
  - [ ] Sidebar visible
  - [ ] Quick prompts work
  - [ ] Messages display correctly
  - [ ] Clear history works
- [ ] Test Appointments Page
  - [ ] Form loads
  - [ ] Can fill all fields
  - [ ] Date picker works
  - [ ] Time slots select
  - [ ] Form submits
  - [ ] Success screen shows
- [ ] Test Admin Panel
  - [ ] Page loads at `/admin`
  - [ ] Can login with `ADMIN_SECRET`
  - [ ] Appointments table shows
  - [ ] Status filter works
  - [ ] Can change status
  - [ ] Can copy emails

#### Discord Bot Testing
- [ ] Start bot: `python run_discord_bot.py`
- [ ] Check console: "✅ ... Discord Bot online"
- [ ] Invite bot to test server (URL from Developer Portal)
- [ ] Test Commands
  - [ ] `/help` shows all commands
  - [ ] `/chat hello` responds
  - [ ] `/book` starts appointment flow
  - [ ] Can complete booking in DM
  - [ ] `/appointments` shows list (admin only)
  - [ ] `/clear` clears history
- [ ] Test DM Chat
  - [ ] Send message in DM
  - [ ] Bot responds with AI
  - [ ] Send crisis keyword test
  - [ ] Owner gets DM alert
  - [ ] Send empathy keyword test
  - [ ] Owner gets DM alert
- [ ] Verify Database
  - [ ] Check `spring_office.db` created
  - [ ] Appointments in DB
  - [ ] Conversations in DB

### ✅ Code Review (10 min)
- [ ] No API keys hardcoded in files
- [ ] `.env` not in git (check `.gitignore`)
- [ ] All imports working
- [ ] No console errors
- [ ] No database errors
- [ ] Crisis keywords seem comprehensive
- [ ] System prompt matches business

### ✅ UI/UX Polish (15 min)
- [ ] Homepage looks professional
- [ ] All text is correct (spell check)
- [ ] Colors match brand
- [ ] Fonts load correctly
- [ ] Mobile responsive (test on phone)
- [ ] Admin panel clear and usable
- [ ] Error messages helpful
- [ ] Animations smooth (no jank)

---

## Pre-Deployment Checklist

### ✅ Security (10 min)
- [ ] `.env` file NOT tracked in git
- [ ] `ADMIN_SECRET` is strong (20+ chars recommended)
- [ ] OPENAI_API_KEY is valid
- [ ] DISCORD_TOKEN hasn't been exposed
- [ ] OWNER_EMAIL is correct
- [ ] Database will be private on server

### ✅ Deployment Prep (10 min)

#### For Railway.app
- [ ] Have GitHub account ready
- [ ] Create GitHub repo (push your code)
- [ ] Create Railway account
- [ ] Have API keys ready to paste

#### For Heroku
- [ ] Have GitHub account ready
- [ ] Create Heroku account
- [ ] Install Heroku CLI (optional)

#### For Self-hosted
- [ ] Have VPS created (DigitalOcean, Linode, etc.)
- [ ] SSH access confirmed
- [ ] Domain ready (optional)
- [ ] Nginx installed (if needed)

### ✅ Git Setup (5 min)
- [ ] Create `.gitignore`:
  ```
  .env
  venv/
  __pycache__/
  *.db
  .DS_Store
  ```
- [ ] Commit all files (except those above)
- [ ] Push to GitHub

---

## Deployment Steps

### 🚀 Option 1: Railway (Recommended)

#### Step 1: Create GitHub Repo
```bash
git init
git add .
git commit -m "Initial commit: Spring Virtual Office"
git remote add origin https://github.com/YOUR_USERNAME/spring-virtual-office.git
git push -u origin main
```

#### Step 2: Deploy on Railway
- [ ] Go to [railway.app](https://railway.app)
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub"
- [ ] Authorize GitHub
- [ ] Select your `spring-virtual-office` repo
- [ ] Click "Deploy"
- [ ] Railway auto-detects Python + FastAPI
- [ ] Wait for build (~2 min)
- [ ] Check deployment logs

#### Step 3: Add Environment Variables
- [ ] In Railway, go to "Variables"
- [ ] Add all from `.env`:
  ```
  OPENAI_API_KEY=sk-...
  DISCORD_TOKEN=MTA...
  OWNER_DISCORD_ID=123456789
  OWNER_EMAIL=you@example.com
  BUSINESS_NAME=Your Business
  ADMIN_SECRET=your-strong-password
  DB_PATH=spring_office.db
  ```
- [ ] Save and redeploy

#### Step 4: Verify Deployment
- [ ] Check "Deployments" tab → latest is "Success"
- [ ] Copy the generated URL
- [ ] Visit URL in browser
- [ ] Homepage should load
- [ ] Check `/admin` works
- [ ] Check chat works

### 🚀 Option 2: Heroku

#### Step 1: Create Heroku App
```bash
heroku login
heroku create your-app-name
```

#### Step 2: Add Buildpack
```bash
heroku buildpacks:add heroku/python
```

#### Step 3: Set Environment Variables
```bash
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set DISCORD_TOKEN=MTA...
heroku config:set OWNER_DISCORD_ID=123456789
heroku config:set OWNER_EMAIL=you@example.com
heroku config:set BUSINESS_NAME="Your Business"
heroku config:set ADMIN_SECRET=your-password
```

#### Step 4: Deploy
```bash
git push heroku main
```

#### Step 5: Verify
- [ ] Check `heroku logs --tail`
- [ ] Visit `https://your-app-name.herokuapp.com`
- [ ] Test all pages

### 🚀 Option 3: Self-hosted (VPS)

#### Step 1: SSH into VPS
```bash
ssh root@your.ip.address
```

#### Step 2: Install Dependencies
```bash
apt update && apt upgrade -y
apt install python3 python3-pip python3-venv git nginx -y
```

#### Step 3: Clone Repository
```bash
cd /opt
git clone https://github.com/YOUR_USERNAME/spring-virtual-office.git
cd spring-virtual-office
```

#### Step 4: Setup & Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 5: Create .env
```bash
nano .env
# Paste your environment variables
```

#### Step 6: Setup Systemd Service
```bash
sudo nano /etc/systemd/system/spring-office.service
```

Add:
```ini
[Unit]
Description=Spring Virtual Office
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/spring-virtual-office
Environment="PATH=/opt/spring-virtual-office/venv/bin"
ExecStart=/opt/spring-virtual-office/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable spring-office
sudo systemctl start spring-office
```

#### Step 7: Setup Nginx
```bash
sudo nano /etc/nginx/sites-available/spring-office
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/spring-office /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 8: SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

#### Step 9: Verify
- [ ] Visit `https://yourdomain.com`
- [ ] Check all pages work
- [ ] Check Discord bot connects

---

## Post-Deployment Checklist

### ✅ Verify Live Site (10 min)
- [ ] Homepage loads: `https://yoursite.com`
- [ ] Chat works: send message
- [ ] Appointments form submits
- [ ] Admin panel loads: `https://yoursite.com/admin`
- [ ] Admin login works
- [ ] Appointments appear in admin

### ✅ Verify Discord Bot (10 min)
- [ ] Bot online in Discord server
- [ ] `/help` shows commands
- [ ] `/chat hello` responds
- [ ] Can complete `/book` flow
- [ ] Owner receives appointment DM
- [ ] Crisis alert works
- [ ] Empathy alert works

### ✅ Share & Announce (5 min)
- [ ] Save website URL
- [ ] Share with team
- [ ] Share with test users
- [ ] Add to marketing materials
- [ ] Update social media
- [ ] Tell customers it's live

### ✅ Monitoring Setup (5 min)
- [ ] Check site daily for first week
- [ ] Monitor admin panel for appointments
- [ ] Check Discord DMs for alerts
- [ ] Watch logs for errors
- [ ] Monitor OpenAI API usage

---

## First Week Checklist

- [ ] Check admin panel daily
- [ ] Review all appointments
- [ ] Respond to client appointments
- [ ] Monitor bot responses
- [ ] Check for any errors
- [ ] Get user feedback
- [ ] Make minor tweaks if needed

---

## Ongoing Maintenance

### Weekly
- [ ] Check appointments
- [ ] Verify bot uptime
- [ ] Review error logs
- [ ] Update status of pending appointments

### Monthly
- [ ] Review OpenAI usage
- [ ] Update dependencies (if needed): `pip list --outdated`
- [ ] Backup database
- [ ] Analyze conversation patterns
- [ ] Get feedback from team

### Quarterly
- [ ] Review and improve system prompt
- [ ] Add new features based on user requests
- [ ] Update crisis/empathy keywords if needed
- [ ] Scale infrastructure if needed

---

## Troubleshooting During Launch

### Website Won't Load
- [ ] Check Railway/Heroku logs
- [ ] Verify environment variables set
- [ ] Ensure all files copied correctly
- [ ] Check folder structure matches

### Chat Returns Errors
- [ ] Verify OPENAI_API_KEY is valid
- [ ] Check OpenAI API status: https://status.openai.com
- [ ] Check API key hasn't hit rate limits
- [ ] Review error logs for details

### Bot Won't Connect
- [ ] Verify DISCORD_TOKEN is correct
- [ ] Check bot has proper permissions
- [ ] Verify Message Content Intent enabled
- [ ] Check bot is in the right server
- [ ] Review bot logs for errors

### Appointments Not Saving
- [ ] Check database file exists
- [ ] Verify folder permissions
- [ ] Check database isn't corrupted
- [ ] Look at error logs
- [ ] Delete DB and let it recreate

### Admin Panel Locked Out
- [ ] Verify ADMIN_SECRET in .env
- [ ] Make sure you're using correct secret
- [ ] Check browser console for errors
- [ ] Try different browser
- [ ] Clear cookies and try again

---

## Success Indicators 🎉

You'll know launch was successful when:

✅ Website loads in under 2 seconds
✅ Chat responds to messages
✅ Appointments appear in admin panel instantly
✅ Discord bot responds to all commands
✅ Owner receives appointment DMs
✅ Crisis alerts trigger correctly
✅ No errors in logs (or only expected ones)
✅ Multiple test users can use the system
✅ Mobile version is responsive
✅ Admin can manage appointments easily

---

## Celebration Moment

When everything is working:

- [ ] Take a screenshot of the live site
- [ ] Check Discord bot is responding
- [ ] View appointment in admin panel
- [ ] 🎉 **You're live!**

---

## Support & Next Steps

### If You Need Help
1. Check logs: `heroku logs --tail` or `journalctl -u spring-office -f`
2. Review error messages carefully
3. Check `.env` variables are correct
4. Verify API keys are valid
5. Read README.md and ARCHITECTURE.md

### Next Features to Add
- Email notifications (Mailgun, SendGrid)
- Calendar integration (Google Calendar)
- Video calls (Zoom, Jitsi)
- Multi-language support
- Analytics dashboard
- Custom branding per client

---

**You did it! Your AI virtual office is now live. Welcome to the future. 🚀🌿**
