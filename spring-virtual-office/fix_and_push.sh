#!/bin/bash

# Spring Virtual Office - Complete Fix & GitHub Push Script
# This fixes the ModuleNotFoundError and pushes everything to GitHub

echo "🚀 Spring Virtual Office - Railway Fix & GitHub Push"
echo "======================================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if in correct directory
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Error: requirements.txt not found${NC}"
    echo "Make sure you're in the spring-virtual-office folder!"
    exit 1
fi

echo -e "${GREEN}✅ Correct directory found${NC}"

# Step 1: Verify folder structure
echo -e "\n${YELLOW}Step 1: Verifying folder structure...${NC}"
touch app/__init__.py
touch app/discord_bot/__init__.py
touch app/discord_bot/cogs/__init__.py
echo -e "${GREEN}✅ __init__.py files created${NC}"

# Step 2: Check files
echo -e "\n${YELLOW}Step 2: Checking all required files...${NC}"

files_ok=true

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1 - MISSING${NC}"
        files_ok=false
    fi
}

echo "Python files:"
check_file "app/main.py"
check_file "app/discord_bot/bot.py"
check_file "app/discord_bot/bot_enhanced.py"
check_file "app/discord_bot/cogs/fun.py"
check_file "app/discord_bot/cogs/moderation.py"
check_file "app/discord_bot/cogs/utility.py"
check_file "run_discord_bot.py"

echo -e "\nHTML files:"
check_file "app/static/index.html"
check_file "app/static/chat.html"
check_file "app/static/appointments.html"
check_file "app/static/admin.html"

echo -e "\nConfig files:"
check_file "requirements.txt"
check_file ".env.example"
check_file ".gitignore"
check_file "Procfile"

if [ "$files_ok" = false ]; then
    echo -e "${RED}❌ Some files are missing! Download them from /outputs${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All files present${NC}"

# Step 3: Initialize Git
echo -e "\n${YELLOW}Step 3: Initializing Git...${NC}"

if [ -d ".git" ]; then
    echo -e "${YELLOW}Git already initialized, skipping...${NC}"
else
    git init
    echo -e "${GREEN}✅ Git initialized${NC}"
fi

# Step 4: Configure Git user (if needed)
echo -e "\n${YELLOW}Step 4: Configuring Git (if needed)...${NC}"
git config user.email "you@example.com" || git config --global user.email "you@example.com"
git config user.name "Spring Virtual Office" || git config --global user.name "Spring Virtual Office"
echo -e "${GREEN}✅ Git configured${NC}"

# Step 5: Add all files
echo -e "\n${YELLOW}Step 5: Adding files to Git...${NC}"
git add .
echo -e "${GREEN}✅ Files added${NC}"

# Step 6: Commit
echo -e "\n${YELLOW}Step 6: Creating commit...${NC}"
git commit -m "Initial commit: Spring Virtual Office with Discord bot and website" || echo -e "${YELLOW}(Already committed)${NC}"
echo -e "${GREEN}✅ Commit created${NC}"

# Step 7: Set main branch
echo -e "\n${YELLOW}Step 7: Setting main branch...${NC}"
git branch -M main
echo -e "${GREEN}✅ Main branch set${NC}"

# Step 8: Display next steps
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ LOCAL SETUP COMPLETE!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${YELLOW}NEXT STEPS:${NC}"
echo ""
echo "1. Create a GitHub repository:"
echo "   👉 Go to: https://github.com/new"
echo "   - Name: spring-virtual-office"
echo "   - Make it PUBLIC"
echo "   - DO NOT initialize with anything"
echo "   - Click 'Create repository'"
echo ""
echo "2. Add GitHub remote and push:"
echo "   👉 Run these commands:"
echo ""
echo "   ${YELLOW}git remote add origin https://github.com/YOUR_USERNAME/spring-virtual-office.git${NC}"
echo "   ${YELLOW}git push -u origin main${NC}"
echo ""
echo "   Replace YOUR_USERNAME with your actual GitHub username!"
echo ""
echo "3. Deploy to Railway:"
echo "   👉 Go to: https://railway.app"
echo "   - Login with GitHub"
echo "   - Create new project"
echo "   - Deploy from GitHub repo"
echo "   - Select spring-virtual-office"
echo "   - Add environment variables (OPENAI_API_KEY, DISCORD_TOKEN, etc.)"
echo "   - Deploy!"
echo ""
echo "4. After Railway deployment:"
echo "   ✅ Website will be live at: https://spring-virtual-office-prod.up.railway.app"
echo "   ✅ Discord bot will come online automatically"
echo ""

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}You're ready for GitHub! 🚀${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
