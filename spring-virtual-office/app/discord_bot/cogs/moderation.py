"""
Moderation Cog — Server moderation tools
Includes: warn, kick, ban, mute, slowmode
"""

import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime

DB_PATH = "spring_office.db"

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_user_warnings(self, user_id: str) -> int:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT warnings FROM user_profiles WHERE user_id=?", (user_id,))
            result = c.fetchone()
            conn.close()
            return result[0] if result else 0
        except:
            return 0
    
    def add_warning(self, user_id: str):
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            warnings = self.get_user_warnings(user_id) + 1
            c.execute("UPDATE user_profiles SET warnings=? WHERE user_id=?", (warnings, user_id))
            if c.rowcount == 0:
                c.execute("INSERT INTO user_profiles (user_id, username, warnings) VALUES (?,?,?)",
                         (user_id, "unknown", warnings))
            conn.commit()
            conn.close()
            return warnings
        except Exception as e:
            print(f"Error adding warning: {e}")
            return 0
    
    @app_commands.command(name="warn", description="Warn a user (mod only)")
    @app_commands.describe(user="User to warn", reason="Reason for warning")
    async def warn_user(self, interaction: discord.Interaction, user: discord.User, reason: str):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
            return

        warnings = self.add_warning(str(user.id))
        
        embed = discord.Embed(
            title="⚠️ Warning Issued",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="User", value=user.mention, inline=True)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Total Warnings", value=f"{warnings}/3", inline=True)
        
        if warnings >= 3:
            embed.description = "⚠️ User has reached 3 warnings. Consider further action."
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="kick", description="Kick a user (mod only)")
    @app_commands.describe(user="User to kick", reason="Reason for kick")
    async def kick_user(self, interaction: discord.Interaction, user: discord.User, reason: str):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
            return

        try:
            await interaction.guild.kick(user, reason=reason)
            embed = discord.Embed(
                title="👢 User Kicked",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="User", value=str(user), inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="ban", description="Ban a user (mod only)")
    @app_commands.describe(user="User to ban", reason="Reason for ban")
    async def ban_user(self, interaction: discord.Interaction, user: discord.User, reason: str):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
            return

        try:
            await interaction.guild.ban(user, reason=reason)
            embed = discord.Embed(
                title="🚫 User Banned",
                color=discord.Color.dark_red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="User", value=str(user), inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="slowmode", description="Set slowmode for channel (mod only)")
    @app_commands.describe(seconds="Slowmode delay in seconds (0 to disable)")
    async def set_slowmode(self, interaction: discord.Interaction, seconds: int = 0):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
            return

        try:
            await interaction.channel.edit(slowmode_delay=seconds)
            if seconds == 0:
                await interaction.response.send_message("✅ Slowmode disabled")
            else:
                await interaction.response.send_message(f"✅ Slowmode set to {seconds}s")
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="warnings", description="Check a user's warnings")
    @app_commands.describe(user="User to check")
    async def check_warnings(self, interaction: discord.Interaction, user: discord.User):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
            return

        warnings = self.get_user_warnings(str(user.id))
        embed = discord.Embed(
            title=f"⚠️ {user.name}'s Warnings",
            description=f"Total warnings: **{warnings}/3**",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
