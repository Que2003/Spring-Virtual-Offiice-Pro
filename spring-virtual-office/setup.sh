#!/bin/bash
# Spring Virtual Office — Quick Setup Script

echo "🌿 Spring Virtual Office Setup"
echo "================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create venv
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate 2>/dev/null || venv\Scripts\activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Setup .env
echo ""
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   Created .env file"
    echo "   ⚠️  IMPORTANT: Edit .env with your API keys:"
    echo "      - OPENAI_API_KEY"
    echo "      - DISCORD_TOKEN"
    echo "      - OWNER_DISCORD_ID"
else
    echo "   .env already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Edit .env with your API keys"
echo "   2. Run the web server: uvicorn app.main:app --reload"
echo "   3. Run the Discord bot: python run_discord_bot.py"
echo "   4. Open http://localhost:8000"
echo ""
echo "📖 Full guide: https://github.com/Que2003/Spring-Virtual-Office"
