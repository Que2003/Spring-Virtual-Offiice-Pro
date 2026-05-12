# 🚀 DEPLOYMENT GUIDE — Where & How to Deploy

## Quick Answer

**Best for beginners:** Railway.app (5 minutes)
**Alternative:** Heroku (10 minutes)
**Advanced:** Self-hosted VPS (30 minutes)

---

## Option 1: Railway.app (RECOMMENDED) ⭐

### Why Railway?
✅ Free tier available
✅ Easiest setup (5 minutes)
✅ Auto-deploys from GitHub
✅ Includes PostgreSQL if needed
✅ Perfect for beginners
✅ Auto-scaling
✅ Perfect for Discord bots

### Step-by-Step: Deploy to Railway

#### 1. Create GitHub Repository
```bash
cd spring-virtual-office
git init
git add .
git commit -m "Initial commit: Spring Virtual Office"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/spring-virtual-office.git
git push -u origin main
```

**Need GitHub account?** Go to github.com and sign up (free)

#### 2. Go to Railway.app
1. Visit https://railway.app
2. Click "Login with GitHub" (or sign up)
3. Authorize Railway to access your GitHub

#### 3. Create New Project
1. Click "New Project" (or "+ New")
2. Select "Deploy from GitHub repo"
3. Select your `spring-virtual-office` repo
4. Click "Deploy"
5. Railway auto-detects Python + FastAPI ✅

#### 4. Add Environment Variables
1. In Railway dashboard, go to "Variables" tab
2. Click "Raw Editor"
3. Paste your environment variables:
```
OPENAI_API_KEY=sk-your-key-here
DISCORD_TOKEN=MTA-your-token-here
OWNER_DISCORD_ID=123456789
OWNER_EMAIL=your@email.com
BUSINESS_NAME=Spring Virtual Office
ADMIN_SECRET=your-strong-password
DB_PATH=spring_office.db
```
4. Click "Save"
5. Railway redeploys automatically

#### 5. Get Your URL
1. In "Deployments" tab, find your live deployment
2. Click the URL (looks like: `spring-virtual-office-production.up.railway.app`)
3. Test it: Website should load! ✅

#### 6. Update Discord Bot
Your bot will automatically work because it uses the environment variables!

#### 7. Verify Deployment
- Website loads: `https://your-app.railway.app` ✅
- Chat works: `/chat hello` ✅
- Appointments work: `/book` ✅
- Admin accessible: `/admin` ✅

**You're live! 🎉 Total time: ~5 minutes**

### Railway Dashboard
After deployment, you get:
- 📊 Live logs
- 🔄 Auto-redeploy on GitHub push
- 📈 Performance metrics
- 🔐 Environment variables
- 🗑️ Easy deletion

---

## Option 2: Heroku (Alternative)

### Why Heroku?
✅ Simple interface
✅ 10-minute setup
✅ Good alternative to Railway
✅ Works great for Discord bots
⚠️ Free tier may be ending soon

### Step-by-Step: Deploy to Heroku

#### 1. Prepare Your Repo
Make sure you have a `Procfile` in root:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
worker: python run_discord_bot.py
```

If not, create it:
```bash
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile
echo "worker: python run_discord_bot.py" >> Procfile
git add Procfile
git commit -m "Add Procfile"
git push
```

#### 2. Create Heroku Account
1. Visit https://heroku.com
2. Sign up (free account)
3. Verify email

#### 3. Deploy via GitHub
1. In Heroku dashboard, click "New" → "Create new app"
2. Name your app: `spring-virtual-office-YOURNAME`
3. Click "Create app"
4. Go to "Deploy" tab
5. Select "GitHub" as deployment method
6. Search for your repo: `spring-virtual-office`
7. Click "Connect"
8. Click "Enable Automatic Deploys" (optional)
9. Click "Deploy Branch"
10. Wait for build to complete (~2 minutes)

#### 4. Add Environment Variables
1. Go to "Settings" tab
2. Click "Reveal Config Vars"
3. Add each variable:
   - `OPENAI_API_KEY` = `sk-...`
   - `DISCORD_TOKEN` = `MTA...`
   - `OWNER_DISCORD_ID` = `123456789`
   - `OWNER_EMAIL` = `your@email.com`
   - `BUSINESS_NAME` = `Spring Virtual Office`
   - `ADMIN_SECRET` = `your-password`
4. Click "Add" for each

#### 5. Scale Dynos (Run Services)
1. Go to "Resources" tab
2. For website: Toggle "web" dyno on
3. For bot: Toggle "worker" dyno on (if available)
4. Confirm changes

#### 6. Get Your URL
1. Go to "Settings"
2. Under "Domains", your URL is: `https://spring-virtual-office-YOURNAME.herokuapp.com`
3. Test it!

#### 7. View Logs
Click "More" → "View Logs" to see what's running

**You're live! 🎉 Total time: ~10 minutes**

---

## Option 3: Self-Hosted VPS (Advanced)

### Why Self-Host?
✅ Full control
✅ No vendor lock-in
✅ Cheaper at scale
✅ Custom domain
✅ Unlimited scale
⚠️ Requires Linux knowledge

### Which VPS Provider?
Pick one:
- **DigitalOcean** — $5/month, easiest
- **Linode** — $5/month, reliable
- **AWS Lightsail** — $3.50/month, more complex
- **Vultr** — $2.50/month, good value
- **Your own server** — Can be cheaper

### Step-by-Step: Deploy to VPS

#### 1. Create VPS Instance
Example (DigitalOcean):
1. Go to https://digitalocean.com
2. Click "Create" → "Droplets"
3. Choose Ubuntu 22.04
4. Choose $5/month plan
5. Create droplet
6. Get your IP address (e.g., `123.45.67.89`)

#### 2. SSH Into Server
```bash
ssh root@123.45.67.89
# Enter password from DigitalOcean email
```

#### 3. Update System
```bash
apt update
apt upgrade -y
```

#### 4. Install Dependencies
```bash
apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx
```

#### 5. Clone Your Repo
```bash
cd /opt
git clone https://github.com/YOUR_USERNAME/spring-virtual-office.git
cd spring-virtual-office
```

#### 6. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 7. Create .env File
```bash
nano .env
# Paste your environment variables
# Press Ctrl+X, then Y, then Enter to save
```

#### 8. Setup Systemd Service
Create `/etc/systemd/system/spring-office.service`:
```bash
sudo nano /etc/systemd/system/spring-office.service
```

Paste this:
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
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save: Ctrl+X, Y, Enter

#### 9. Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable spring-office
sudo systemctl start spring-office
sudo systemctl status spring-office
```

Should show "active (running)" ✅

#### 10. Setup Nginx (Reverse Proxy)
Create `/etc/nginx/sites-available/spring-office`:
```bash
sudo nano /etc/nginx/sites-available/spring-office
```

Paste this:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:
```bash
sudo ln -s /etc/nginx/sites-available/spring-office /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 11. Setup SSL (HTTPS)
```bash
sudo certbot --nginx -d your-domain.com
# Follow prompts, select auto-renew
```

#### 12. Deploy Bot (in separate terminal/screen)
```bash
# SSH into server again in another tab
ssh root@123.45.67.89
cd /opt/spring-virtual-office
source venv/bin/activate
python run_discord_bot.py
```

Or create another systemd service for the bot:
```bash
sudo nano /etc/systemd/system/spring-office-bot.service
```

```ini
[Unit]
Description=Spring Virtual Office Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/spring-virtual-office
Environment="PATH=/opt/spring-virtual-office/venv/bin"
ExecStart=/opt/spring-virtual-office/venv/bin/python run_discord_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start it:
```bash
sudo systemctl enable spring-office-bot
sudo systemctl start spring-office-bot
sudo systemctl status spring-office-bot
```

#### 13. Verify
- Website: `https://your-domain.com` ✅
- Chat works: `/chat hello` ✅
- Bot online: Check Discord ✅

**You're live! 🎉 Total time: ~30 minutes**

---

## Comparison Table

| Feature | Railway | Heroku | VPS |
|---------|---------|--------|-----|
| **Setup Time** | 5 min | 10 min | 30 min |
| **Cost** | Free tier available | Free (may end) | $5+/month |
| **Difficulty** | ⭐ Easy | ⭐⭐ Medium | ⭐⭐⭐ Hard |
| **Scaling** | Auto | Manual | Manual |
| **Custom Domain** | Paid | Free | Free |
| **HTTPS** | Automatic | Automatic | Free (Let's Encrypt) |
| **Uptime** | 99.9% | 99.9% | Depends on you |
| **PostgreSQL** | Yes | Yes | Add separately |
| **Recommendation** | ✅ BEST | Alternative | Advanced |

---

## Environment Variables (All Platforms)

No matter which platform, you need these in "Environment Variables" or "Config Vars":

```
OPENAI_API_KEY=sk-your-actual-key
DISCORD_TOKEN=MTA-your-actual-token
OWNER_DISCORD_ID=your-discord-id-number
OWNER_EMAIL=your@email.com
BUSINESS_NAME=Spring Virtual Office
ADMIN_SECRET=strong-password-here
DB_PATH=spring_office.db
```

Where to get them:
- **OPENAI_API_KEY** → https://openai.com/account/api-keys
- **DISCORD_TOKEN** → https://discord.com/developers/applications
- **OWNER_DISCORD_ID** → Right-click username in Discord (Developer Mode on)
- **OWNER_EMAIL** → Your email
- **BUSINESS_NAME** → Your company name
- **ADMIN_SECRET** → Create a strong password
- **DB_PATH** → Usually `spring_office.db`

---

## How to Get Discord Token

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name it "Spring Virtual Office"
4. Go to "Bot" tab
5. Click "Add Bot"
6. Copy the token under "TOKEN"
7. Paste into DISCORD_TOKEN

⚠️ **IMPORTANT:** Never share this token! Treat it like a password!

---

## How to Get OpenAI API Key

1. Go to https://openai.com/account/api-keys
2. Log in (create account if needed)
3. Click "Create new secret key"
4. Copy the key
5. Paste into OPENAI_API_KEY

⚠️ **IMPORTANT:** Never commit this key! Use .env file only!

---

## Troubleshooting Deployment

### Website won't load
1. Check environment variables are set
2. Check logs for errors
3. Verify database file exists
4. Restart the service

### Bot won't come online
1. Check DISCORD_TOKEN is correct
2. Check bot has Message Content Intent enabled
3. Check bot is in your server
4. Check logs for errors

### "Permission denied" errors
1. Make sure bot has proper permissions in Discord
2. Make sure systemd service runs as correct user
3. Check folder/file permissions

### Database errors
1. Delete `spring_office.db` (it recreates)
2. Verify write permissions
3. Check disk space

### SSL/HTTPS errors (self-hosted)
1. Run certbot: `sudo certbot --nginx`
2. Check DNS points to your server
3. Wait for DNS propagation (24 hours)

---

## Custom Domain (All Platforms)

### Railway
1. Go to "Settings"
2. Add custom domain
3. Update DNS settings
4. Wait for verification

### Heroku
1. Go to "Settings"
2. Add domain
3. Update DNS to Heroku's servers
4. Wait for verification

### VPS
1. Buy domain (Namecheap, GoDaddy, etc.)
2. Point DNS to your VPS IP
3. Use Let's Encrypt for SSL
4. Should work immediately!

---

## Monitoring Your Deployment

### Railway
- Dashboard shows live logs
- Click "Metrics" for performance
- Auto-alerts for crashes

### Heroku
- Click "View Logs" for live logs
- View usage metrics in Resources
- Set up alerts in settings

### VPS
```bash
# Check if services running
sudo systemctl status spring-office
sudo systemctl status spring-office-bot

# View logs
sudo journalctl -u spring-office -f
sudo journalctl -u spring-office-bot -f

# Check disk space
df -h

# Check memory
free -h
```

---

## Backup Your Database

### Railway
Automatic daily backups included

### Heroku
Use pgBackups or manual dumps

### VPS
```bash
# Backup database
cp spring_office.db spring_office.db.backup

# Or via cron (automatic daily):
0 2 * * * cp /opt/spring-virtual-office/spring_office.db /backups/spring_office.db.$(date +\%Y\%m\%d)
```

---

## Scale When You Grow

### If you get slow response times:
- **Railway:** Auto-scales
- **Heroku:** Upgrade dyno size
- **VPS:** Upgrade to bigger server or add database server

### If you get database issues:
- **Railway:** Add PostgreSQL
- **Heroku:** Add PostgreSQL add-on
- **VPS:** Migrate to separate PostgreSQL server

### If Discord bot gets slow:
- Run bot on separate dyno/service
- Use task queue system
- Add caching

---

## My Recommendation

**For beginners:** Railway.app (easiest, free tier, best DX)
**For learning:** Heroku (simple, educational)
**For production:** Railway.app (reliable) or self-hosted VPS (full control)

---

## Deploy Right Now

### 30-Second Quickstart (Railway)

1. **GitHub:** Push your repo to GitHub
2. **Railway.app:** Sign in with GitHub
3. **Deploy:** Click "New Project" → Select repo → Deploy
4. **Variables:** Add OPENAI_API_KEY, DISCORD_TOKEN, etc.
5. **Done:** Your URL is live!

**That's it. Really.**

---

## Need Help?

| Issue | Check |
|-------|-------|
| Environment variables missing | See "Environment Variables" section |
| Bot won't start | See "Troubleshooting" section |
| Website won't load | Check logs in platform dashboard |
| Domain not working | Check DNS settings |
| Database errors | Delete DB and restart |

---

## Quick Links

- **Railway:** https://railway.app
- **Heroku:** https://heroku.com
- **DigitalOcean:** https://digitalocean.com
- **OpenAI API:** https://openai.com/account/api-keys
- **Discord Developers:** https://discord.com/developers
- **Let's Encrypt:** https://letsencrypt.org

---

**You have three options. Pick one. Deploy in 5-30 minutes. You're live!** 🚀

**Recommended: Railway.app (easiest, fastest, best for beginners)**
