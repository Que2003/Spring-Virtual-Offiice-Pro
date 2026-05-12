"""
Spring Virtual Office — Enhanced Discord Bot
Integrates all SpringBot features: moderation, utility, writing, empathy, 
fun, news, information, study, welcome, music, and more
"""

import discord
from discord.ext import commands, tasks
import os
import json
import sqlite3
import asyncio
from datetime import datetime
from openai import AsyncOpenAI
import random
import aiohttp
from urllib.parse import quote

# ─── Config ────────────────────────────────────────────────────────────────────
DISCORD_TOKEN     = os.getenv("DISCORD_TOKEN", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
OWNER_DISCORD_ID  = int(os.getenv("OWNER_DISCORD_ID", "0"))
BUSINESS_NAME     = os.getenv("BUSINESS_NAME", "Spring Virtual Office")

client_ai = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Keywords for detection
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "self harm",
    "hurt myself", "no reason to live", "can't go on", "hopeless"
]

EMPATHY_KEYWORDS = [
    "stressed", "overwhelmed", "anxious", "depressed", "frustrated",
    "sad", "scared", "panic", "crying", "lost", "struggling"
]

SYSTEM_PROMPT = f"""You are the AI assistant for {BUSINESS_NAME}, a professional virtual office platform.
You help users with:
- General business questions and support
- Scheduling appointments
- Empathetic assistance
- Fun commands and engagement
- Writing and learning help
- News and information
- Study resources
- Music recommendations

Be warm, professional, helpful, and engaging. Keep responses under 200 words unless asked for detail."""

DB_PATH = os.getenv("DB_PATH", "spring_office.db")

# ─── Data Storage ──────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_user TEXT,
            name TEXT,
            email TEXT,
            preferred_time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_user TEXT,
            role TEXT,
            content TEXT,
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            level INTEGER DEFAULT 1,
            points INTEGER DEFAULT 0,
            warnings INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS study_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            topic TEXT,
            notes TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_json(filename):
    """Load or create JSON file for storage"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Load data files
economy_data = load_json("economy.json")
inventory_data = load_json("inventory.json")
study_notes = load_json("study_notes.json")

# ─── Bot Setup ─────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

appointment_sessions: dict[int, dict] = {}

# ─── AI Helper ─────────────────────────────────────────────────────────────────
async def get_ai_response(user_id: str, user_message: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM conversations WHERE discord_user=? ORDER BY id DESC LIMIT 10",
              (user_id,))
    history = list(reversed(c.fetchall()))
    conn.close()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for role, content in history:
        messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_message})

    try:
        response = await client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Connection issue. Try again shortly. ({str(e)[:60]})"

# ─── Safety Detection ──────────────────────────────────────────────────────────
def detect_crisis(text: str) -> bool:
    return any(kw in text.lower() for kw in CRISIS_KEYWORDS)

def detect_empathy(text: str) -> bool:
    return any(kw in text.lower() for kw in EMPATHY_KEYWORDS)

async def alert_owner(bot_instance: commands.Bot, user: discord.User, message: str, alert_type: str):
    if not OWNER_DISCORD_ID:
        return
    try:
        owner = await bot_instance.fetch_user(OWNER_DISCORD_ID)
        embed = discord.Embed(
            title=f"🚨 {alert_type} — {BUSINESS_NAME}",
            color=discord.Color.red() if alert_type == "CRISIS" else discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="User", value=f"{user} ({user.id})", inline=False)
        embed.add_field(name="Message", value=message[:500], inline=False)
        await owner.send(embed=embed)
    except Exception:
        pass

# ─── Welcome Cog ──────────────────────────────────────────────────────────────
@bot.event
async def on_member_join(member: discord.Member):
    """Welcome new members"""
    try:
        embed = discord.Embed(
            title=f"👋 Welcome {member.name}!",
            description=f"Welcome to {BUSINESS_NAME}! We're glad to have you here.",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Get Started", value="`/help` to see all commands", inline=False)
        embed.add_field(name="Need Support?", value="Use `/chat` to talk with our AI assistant", inline=False)
        
        # Initialize user profile
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""INSERT OR IGNORE INTO user_profiles (user_id, username, created_at)
                     VALUES (?, ?, ?)""",
                  (str(member.id), member.name, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        
        # Send DM
        await member.send(embed=embed)
    except Exception:
        pass

# ─── Moderation Commands ───────────────────────────────────────────────────────
@tree.command(name="warn", description="Warn a user (mod only)")
@app_commands.describe(user="User to warn", reason="Reason for warning")
async def warn_user(interaction: discord.Interaction, user: discord.User, reason: str):
    # Check if moderator
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT warnings FROM user_profiles WHERE user_id=?", (str(user.id),))
    result = c.fetchone()
    warnings = (result[0] if result else 0) + 1
    c.execute("UPDATE user_profiles SET warnings=? WHERE user_id=?", (warnings, str(user.id)))
    conn.commit()
    conn.close()

    embed = discord.Embed(
        title="⚠️ Warning Issued",
        color=discord.Color.orange(),
        description=f"**User:** {user}\n**Reason:** {reason}\n**Total Warnings:** {warnings}"
    )
    await interaction.response.send_message(embed=embed)

@tree.command(name="kick", description="Kick a user (mod only)")
@app_commands.describe(user="User to kick", reason="Reason for kick")
async def kick_user(interaction: discord.Interaction, user: discord.User, reason: str):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return

    try:
        await interaction.guild.kick(user, reason=reason)
        await interaction.response.send_message(f"✅ Kicked {user}: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

# ─── Fun Commands ──────────────────────────────────────────────────────────────
@tree.command(name="joke", description="Get a random joke")
async def tell_joke(interaction: discord.Interaction):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a fake noodle? An impasta!",
        "Why did the math book look sad? Because it had too many problems!",
    ]
    await interaction.response.send_message(f"😄 {random.choice(jokes)}")

@tree.command(name="roll", description="Roll a dice")
@app_commands.describe(sides="Number of sides (default: 6)")
async def roll_dice(interaction: discord.Interaction, sides: int = 6):
    result = random.randint(1, max(2, sides))
    await interaction.response.send_message(f"🎲 You rolled: **{result}** (1-{sides})")

@tree.command(name="flip", description="Flip a coin")
async def flip_coin(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"🪙 **{result}**")

@tree.command(name="8ball", description="Ask the magic 8-ball")
@app_commands.describe(question="Your question")
async def magic_8ball(interaction: discord.Interaction, question: str):
    responses = [
        "Yes definitely", "No way", "Ask again later", "Maybe", "Absolutely",
        "Don't count on it", "Looking good", "Outlook not so good", "Concentrate and ask again"
    ]
    await interaction.response.send_message(f"🔮 **{question}**\n{random.choice(responses)}")

# ─── Utility Commands ──────────────────────────────────────────────────────────
@tree.command(name="userinfo", description="Get user information")
@app_commands.describe(user="User to check (default: yourself)")
async def user_info(interaction: discord.Interaction, user: discord.User = None):
    user = user or interaction.user
    embed = discord.Embed(
        title=f"📋 {user.name}'s Info",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Username", value=user.mention, inline=True)
    embed.add_field(name="User ID", value=user.id, inline=True)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
    await interaction.response.send_message(embed=embed)

@tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000
    await interaction.response.send_message(f"🏓 Pong! **{latency:.0f}ms**")

# ─── News Commands ─────────────────────────────────────────────────────────────
@tree.command(name="news", description="Get latest tech news")
async def get_news(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://newsapi.org/v2/top-headlines?category=technology&pageSize=5") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    embed = discord.Embed(title="📰 Latest Tech News", color=discord.Color.blurple())
                    for article in data.get("articles", [])[:3]:
                        embed.add_field(
                            name=article.get("title", "")[:50],
                            value=article.get("description", "")[:100],
                            inline=False
                        )
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("⚠️ News service unavailable. Try again later.")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)[:100]}")

# ─── Information Commands ──────────────────────────────────────────────────────
@tree.command(name="define", description="Get definition of a word")
@app_commands.describe(word="Word to define")
async def define_word(interaction: discord.Interaction, word: str):
    await interaction.response.defer(thinking=True)
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and len(data) > 0:
                        entry = data[0]
                        definition = entry.get("meanings", [{}])[0].get("definitions", [{}])[0].get("definition", "Not found")
                        embed = discord.Embed(
                            title=f"📚 {entry.get('word', word)}",
                            description=definition,
                            color=discord.Color.green()
                        )
                        if "phonetics" in entry and entry["phonetics"]:
                            embed.add_field(name="Pronunciation", value=entry["phonetics"][0].get("text", "N/A"), inline=False)
                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send(f"❌ Word '{word}' not found.")
                else:
                    await interaction.followup.send(f"❌ Word '{word}' not found.")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)[:100]}")

# ─── Writing Help ──────────────────────────────────────────────────────────────
@tree.command(name="grammar", description="Check grammar and writing")
@app_commands.describe(text="Text to check")
async def check_grammar(interaction: discord.Interaction, text: str):
    await interaction.response.defer(thinking=True)
    prompt = f"Check this for grammar, spelling, and clarity. Provide suggestions:\n\n{text}"
    response = await get_ai_response(str(interaction.user.id), prompt)
    embed = discord.Embed(
        title="✏️ Writing Feedback",
        description=response,
        color=discord.Color.gold()
    )
    await interaction.followup.send(embed=embed)

@tree.command(name="rephrase", description="Rephrase text in different styles")
@app_commands.describe(text="Text to rephrase", style="professional/casual/formal/creative")
async def rephrase_text(interaction: discord.Interaction, text: str, style: str = "professional"):
    await interaction.response.defer(thinking=True)
    prompt = f"Rephrase this in a {style} tone:\n\n{text}"
    response = await get_ai_response(str(interaction.user.id), prompt)
    embed = discord.Embed(
        title=f"🔄 {style.title()} Rephrase",
        description=response,
        color=discord.Color.orange()
    )
    await interaction.followup.send(embed=embed)

# ─── Study Commands ───────────────────────────────────────────────────────────
@tree.command(name="savenote", description="Save a study note")
@app_commands.describe(topic="Topic/subject", note="Your note")
async def save_note(interaction: discord.Interaction, topic: str, note: str):
    user_id = str(interaction.user.id)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO study_notes (user_id, topic, notes, created_at) VALUES (?,?,?,?)",
              (user_id, topic, note, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"✅ Note saved under **{topic}**", ephemeral=True)

@tree.command(name="mynotes", description="View your study notes")
async def view_notes(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT topic, notes FROM study_notes WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    notes = c.fetchall()
    conn.close()

    if not notes:
        await interaction.response.send_message("📝 You have no saved notes yet.", ephemeral=True)
        return

    embed = discord.Embed(title="📚 Your Study Notes", color=discord.Color.purple())
    for topic, note in notes[:5]:
        embed.add_field(name=topic, value=note[:200], inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ─── Chat & Appointments ───────────────────────────────────────────────────────
@tree.command(name="chat", description="Chat with AI assistant")
@app_commands.describe(message="Your message")
async def slash_chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True)
    user = interaction.user

    if detect_crisis(message):
        await alert_owner(bot, user, message, "CRISIS")
        await interaction.followup.send(
            "💙 I'm concerned about what you shared.\n\n"
            "**Crisis Resources:**\n988 Lifeline: Call or text **988**\n"
            "Crisis Text Line: Text **HOME** to **741741**\n"
            "**Emergency: 911**"
        )
        return

    if detect_empathy(message):
        await alert_owner(bot, user, message, "EMPATHY")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO conversations (discord_user, role, content, created_at) VALUES (?,?,?,?)",
              (str(user.id), "user", message, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

    reply = await get_ai_response(str(user.id), message)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO conversations (discord_user, role, content, created_at) VALUES (?,?,?,?)",
              (str(user.id), "assistant", reply, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

    await interaction.followup.send(f"🌿 {reply}")

@tree.command(name="book", description="Book an appointment")
async def slash_book(interaction: discord.Interaction):
    user = interaction.user
    appointment_sessions[user.id] = {"step": "name"}
    await interaction.response.send_message(
        "📅 **Let's book your appointment!**\n\nWhat's your **full name**?",
        ephemeral=True
    )

@tree.command(name="help", description="Show all available commands")
async def show_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"🌿 {BUSINESS_NAME} — Command Guide",
        description="Everything I can do for you:",
        color=discord.Color.teal()
    )
    
    embed.add_field(name="💬 AI & Support", value="`/chat [message]` - Talk with AI\n`/book` - Schedule appointment", inline=False)
    embed.add_field(name="😄 Fun", value="`/joke` - Get a joke\n`/roll [sides]` - Roll dice\n`/flip` - Flip coin\n`/8ball` - Ask magic 8-ball", inline=False)
    embed.add_field(name="📚 Learning", value="`/define [word]` - Define word\n`/grammar [text]` - Check grammar\n`/rephrase [text] [style]` - Rephrase text\n`/savenote [topic] [note]` - Save note\n`/mynotes` - View notes", inline=False)
    embed.add_field(name="📋 Utility", value="`/userinfo [@user]` - User info\n`/ping` - Check latency\n`/news` - Latest tech news", inline=False)
    embed.add_field(name="🛡️ Moderation", value="`/warn [@user] [reason]` - Warn user (mod)\n`/kick [@user] [reason]` - Kick user (mod)", inline=False)
    
    await interaction.response.send_message(embed=embed)

# ─── Message Handler ───────────────────────────────────────────────────────────
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    user = message.author
    content = message.content.strip()

    # Handle appointment flow
    if user.id in appointment_sessions:
        session = appointment_sessions[user.id]
        step = session.get("step")

        if step == "name":
            session["name"] = content
            session["step"] = "email"
            await message.reply("📧 Great! What's your **email address**?")

        elif step == "email":
            session["email"] = content
            session["step"] = "time"
            await message.reply("🕐 When would you like to meet? (e.g. *Tuesday June 10 at 2pm*)")

        elif step == "time":
            session["preferred_time"] = content
            session["step"] = "reason"
            await message.reply("📝 What's the **reason** for your appointment?")

        elif step == "reason":
            session["reason"] = content
            
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                "INSERT INTO appointments (discord_user,name,email,preferred_time,reason,created_at) VALUES (?,?,?,?,?,?)",
                (str(user.id), session["name"], session["email"], session["preferred_time"], session["reason"],
                 datetime.utcnow().isoformat())
            )
            conn.commit()
            conn.close()
            
            del appointment_sessions[user.id]

            embed = discord.Embed(
                title="✅ Appointment Requested!",
                color=discord.Color.green(),
                description="We've received your request and will confirm shortly."
            )
            embed.add_field(name="Name", value=session["name"])
            embed.add_field(name="Email", value=session["email"])
            embed.add_field(name="Time", value=session["preferred_time"])
            embed.add_field(name="Reason", value=session["reason"])
            await message.reply(embed=embed)
        return

    # DM chat
    if isinstance(message.channel, discord.DMChannel):
        if detect_crisis(content):
            await alert_owner(bot, user, content, "CRISIS")
            await message.reply(
                "💙 Please reach out for help:\n\n"
                "**988 Lifeline:** Call or text **988**\n"
                "**Crisis Text Line:** Text **HOME** to **741741**"
            )
            return

        if detect_empathy(content):
            await alert_owner(bot, user, content, "EMPATHY")

        async with message.channel.typing():
            reply = await get_ai_response(str(user.id), content)
        await message.reply(reply)

    await bot.process_commands(message)

# ─── Ready ─────────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    init_db()
    await tree.sync()
    print(f"✅ {BUSINESS_NAME} Enhanced Bot online as {bot.user}")
    print(f"   📋 Modules loaded: moderation, utility, fun, news, writing, study, empathy, welcome")
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{BUSINESS_NAME} | /help"
    )
    await bot.change_presence(activity=activity)

def run_bot():
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN is not set in environment variables.")
    bot.run(DISCORD_TOKEN)
