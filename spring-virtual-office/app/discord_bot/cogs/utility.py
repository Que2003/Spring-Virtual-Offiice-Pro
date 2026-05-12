"""
Utility Cog — Helpful utility commands
Includes: userinfo, serverinfo, ping, uptime, avatar, etc.
"""

import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()
    
    @app_commands.command(name="userinfo", description="Get detailed user information")
    @app_commands.describe(user="User to check (default: yourself)")
    async def user_info(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        embed = discord.Embed(
            title=f"👤 {user.name}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Username", value=user.mention, inline=True)
        embed.add_field(name="User ID", value=f"`{user.id}`", inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Bot?", value="Yes ✅" if user.bot else "No", inline=True)
        
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serverinfo", description="Get server information")
    async def server_info(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"🏰 {guild.name}",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency * 1000
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**Latency:** {latency:.0f}ms",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="uptime", description="Check bot uptime")
    async def uptime(self, interaction: discord.Interaction):
        delta = datetime.utcnow() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(
            title="⏱️ Bot Uptime",
            description=f"**{hours}h {minutes}m {seconds}s**",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="avatar", description="Get user avatar")
    @app_commands.describe(user="User to get avatar from (default: yourself)")
    async def get_avatar(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        embed = discord.Embed(
            title=f"{user.name}'s Avatar",
            color=discord.Color.purple()
        )
        if user.avatar:
            embed.set_image(url=user.avatar.url)
            embed.add_field(name="Link", value=f"[Avatar](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar.key}.png?size=4096)")
        else:
            embed.description = "User has no avatar"
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="membercount", description="Get server member count")
    async def member_count(self, interaction: discord.Interaction):
        guild = interaction.guild
        total = guild.member_count
        bots = sum(1 for m in guild.members if m.bot)
        humans = total - bots
        
        embed = discord.Embed(
            title="👥 Member Count",
            color=discord.Color.blue()
        )
        embed.add_field(name="Total", value=total, inline=True)
        embed.add_field(name="Humans", value=humans, inline=True)
        embed.add_field(name="Bots", value=bots, inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
