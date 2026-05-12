"""
Spring Virtual Office — Cogs Loader
Loads all modular command groups
"""

import discord
from discord.ext import commands
import os
import importlib

class CogsManager:
    """Manages loading and reloading of all cogs"""
    
    def __init__(self, bot):
        self.bot = bot
        self.cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
        
    async def load_all_cogs(self):
        """Load all cogs from cogs directory"""
        if not os.path.exists(self.cogs_dir):
            os.makedirs(self.cogs_dir)
            print(f"📁 Created cogs directory at {self.cogs_dir}")
        
        cogs_list = [f[:-3] for f in os.listdir(self.cogs_dir) 
                     if f.endswith('.py') and not f.startswith('_')]
        
        for cog_name in cogs_list:
            try:
                await self.bot.load_extension(f'app.discord_bot.cogs.{cog_name}')
                print(f"✅ Loaded cog: {cog_name}")
            except Exception as e:
                print(f"❌ Error loading {cog_name}: {str(e)}")
    
    async def reload_cog(self, cog_name):
        """Reload a specific cog"""
        try:
            await self.bot.reload_extension(f'app.discord_bot.cogs.{cog_name}')
            return True, f"Reloaded {cog_name}"
        except Exception as e:
            return False, f"Error: {str(e)}"
