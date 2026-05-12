"""
Spring Virtual Office — Full Discord Bot
Features: AI chat, appointment booking, empathy detection, slash commands, admin panel DMs
"""

import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import sqlite3
import asyncio
from datetime import datetime
from openai import AsyncOpenAI

# ─── Config ────────────────────────────────────────────────────────────────────
DISCORD_TOKEN     = os.getenv("DISCORD_TOKEN", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
OWNER_DISCORD_ID  = int(os.getenv("OWNER_DISCORD_ID", "0"))
BUSINESS_NAME     = os.getenv("BUSINESS_NAME", "Spring Virtual Office")

client_ai = AsyncOpenAI(api_key=OPENAI_API_KEY)

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
- Scheduling appointments (collect name, email, date/time, and reason)
- Empathetic assistance when users are stressed or struggling
- Answering FAQs about the business

When collecting appointment info, ask one question at a time. Be warm, professional, and concise.
Always respond in under 200 words unless the user asks for detail.
If asked about sensitive personal issues beyond your scope, gently suggest speaking to a professional.
"""

# ─── Database ──────────────────────────────────────────────────────────────────
DB_PATH = os.getenv("DB_PATH", "spring_office.db")

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
    conn.commit()
    conn.close()

def save_message(user_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversations (discord_user, role, content, created_at) VALUES (?,?,?,?)",
        (user_id, role, content, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def get_history(user_id: str, limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT role, content FROM conversations WHERE discord_user=? ORDER BY id DESC LIMIT ?",
        (user_id, limit)
    )
    rows = c.fetchall()
    conn.close()
    return list(reversed(rows))

def save_appointment(discord_user, name, email, preferred_time, reason):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO appointments (discord_user,name,email,preferred_time,reason,created_at) VALUES (?,?,?,?,?,?)",
        (discord_user, name, email, preferred_time, reason, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def get_all_appointments():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id,discord_user,name,email,preferred_time,reason,status,created_at FROM appointments ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# ─── Bot Setup ─────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Track multi-step appointment flows per user
appointment_sessions: dict[int, dict] = {}

# ─── AI Helper ─────────────────────────────────────────────────────────────────
async def get_ai_response(user_id: str, user_message: str) -> str:
    history = get_history(user_id)
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
        return f"⚠️ I'm having trouble connecting right now. Please try again shortly. ({str(e)[:60]})"

def detect_crisis(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in CRISIS_KEYWORDS)

def detect_empathy(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in EMPATHY_KEYWORDS)

async def alert_owner(bot_instance: commands.Bot, user: discord.User, message: str, alert_type: str):
    if not OWNER_DISCORD_ID:
        return
    try:
        owner = await bot_instance.fetch_user(OWNER_DISCORD_ID)
        embed = discord.Embed(
            title=f"🚨 {alert_type} Alert — {BUSINESS_NAME}",
            color=discord.Color.red() if alert_type == "CRISIS" else discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="User", value=f"{user} ({user.id})", inline=False)
        embed.add_field(name="Message", value=message[:500], inline=False)
        await owner.send(embed=embed)
    except Exception:
        pass

# ─── Slash Commands ─────────────────────────────────────────────────────────────

@tree.command(name="chat", description="Chat with the Spring Virtual Office AI assistant")
@app_commands.describe(message="Your message or question")
async def slash_chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True)
    user = interaction.user

    if detect_crisis(message):
        await alert_owner(bot, user, message, "CRISIS")
        await interaction.followup.send(
            "💙 I'm concerned about what you shared. Please know you're not alone.\n\n"
            "**Crisis Resources:**\n"
            "• 988 Suicide & Crisis Lifeline: **Call or text 988**\n"
            "• Crisis Text Line: **Text HOME to 741741**\n"
            "• Emergency: **911**\n\n"
            "A team member has also been notified. You matter. 💙"
        )
        return

    if detect_empathy(message):
        await alert_owner(bot, user, message, "EMPATHY")

    save_message(str(user.id), "user", message)
    reply = await get_ai_response(str(user.id), message)
    save_message(str(user.id), "assistant", reply)
    await interaction.followup.send(f"🌿 **{BUSINESS_NAME}**\n\n{reply}")


@tree.command(name="book", description="Book an appointment with Spring Virtual Office")
async def slash_book(interaction: discord.Interaction):
    user = interaction.user
    appointment_sessions[user.id] = {"step": "name"}
    await interaction.response.send_message(
        "📅 **Let's book your appointment!**\n\nWhat's your **full name**?",
        ephemeral=True
    )


@tree.command(name="appointments", description="[Admin] View all pending appointments")
async def slash_appointments(interaction: discord.Interaction):
    if interaction.user.id != OWNER_DISCORD_ID:
        await interaction.response.send_message("❌ This command is for admins only.", ephemeral=True)
        return

    rows = get_all_appointments()
    if not rows:
        await interaction.response.send_message("📋 No appointments found.", ephemeral=True)
        return

    embed = discord.Embed(
        title=f"📋 {BUSINESS_NAME} — Appointments",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    for row in rows[:10]:  # show latest 10
        appt_id, discord_user, name, email, preferred_time, reason, status, created_at = row
        embed.add_field(
            name=f"#{appt_id} — {name} [{status.upper()}]",
            value=f"📧 {email}\n🕐 {preferred_time}\n📝 {reason}\n👤 {discord_user}",
            inline=False
        )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="clear", description="Clear your conversation history with the AI")
async def slash_clear(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM conversations WHERE discord_user=?", (user_id,))
    conn.commit()
    conn.close()
    await interaction.response.send_message("🧹 Your conversation history has been cleared!", ephemeral=True)


@tree.command(name="help", description="Show all Spring Virtual Office bot commands")
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"🌿 {BUSINESS_NAME} — Command Guide",
        description="Here's everything I can do for you:",
        color=discord.Color.teal()
    )
    embed.add_field(name="/chat [message]", value="Ask the AI assistant anything", inline=False)
    embed.add_field(name="/book", value="Schedule an appointment", inline=False)
    embed.add_field(name="/clear", value="Reset your conversation memory", inline=False)
    embed.add_field(name="/appointments", value="[Admin] View all appointments", inline=False)
    embed.add_field(name="/help", value="Show this message", inline=False)
    embed.set_footer(text=f"{BUSINESS_NAME} • Powered by AI")
    await interaction.response.send_message(embed=embed)


# ─── Message Handler (Appointment Flow + DM Chat) ──────────────────────────────

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    user = message.author
    content = message.content.strip()

    # Handle multi-step appointment booking
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
            save_appointment(
                str(user.id),
                session["name"],
                session["email"],
                session["preferred_time"],
                session["reason"]
            )
            del appointment_sessions[user.id]

            # Notify owner
            await alert_owner(
                bot, user,
                f"Name: {session['name']}\nEmail: {session['email']}\n"
                f"Time: {session['preferred_time']}\nReason: {session['reason']}",
                "NEW APPOINTMENT"
            )

            embed = discord.Embed(
                title="✅ Appointment Requested!",
                color=discord.Color.green(),
                description="We've received your appointment request and will confirm it shortly."
            )
            embed.add_field(name="Name", value=session["name"])
            embed.add_field(name="Email", value=session["email"])
            embed.add_field(name="Preferred Time", value=session["preferred_time"])
            embed.add_field(name="Reason", value=session["reason"])
            await message.reply(embed=embed)
        return

    # DM-only AI chat (non-command)
    if isinstance(message.channel, discord.DMChannel):
        if detect_crisis(content):
            await alert_owner(bot, user, content, "CRISIS")
            await message.reply(
                "💙 I'm really concerned about what you shared. Please reach out for help:\n\n"
                "• **988 Lifeline**: Call or text 988\n"
                "• **Crisis Text Line**: Text HOME to 741741\n"
                "• **Emergency**: 911\n\n"
                "You're not alone, and help is available right now. 💙"
            )
            return

        if detect_empathy(content):
            await alert_owner(bot, user, content, "EMPATHY")

        save_message(str(user.id), "user", content)
        async with message.channel.typing():
            reply = await get_ai_response(str(user.id), content)
        save_message(str(user.id), "assistant", reply)
        await message.reply(reply)

    await bot.process_commands(message)


# ─── Ready ─────────────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    init_db()
    await tree.sync()
    print(f"✅ {BUSINESS_NAME} Discord Bot online as {bot.user}")
    print(f"   Slash commands synced globally.")
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{BUSINESS_NAME} | /help"
    )
    await bot.change_presence(activity=activity)


def run_bot():
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN is not set in environment variables.")
    bot.run(DISCORD_TOKEN)
