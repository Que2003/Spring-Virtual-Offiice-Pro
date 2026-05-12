"""
Fun Cog — Fun and engaging commands
Includes: jokes, dice, coin flip, magic 8-ball, memes, etc.
"""

import discord
from discord.ext import commands
from discord import app_commands
import random

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="joke", description="Get a random joke")
    async def tell_joke(self, interaction: discord.Interaction):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
        ]
        await interaction.response.send_message(f"😄 {random.choice(jokes)}")
    
    @app_commands.command(name="roll", description="Roll a dice")
    @app_commands.describe(sides="Number of sides (default: 6)")
    async def roll_dice(self, interaction: discord.Interaction, sides: int = 6):
        result = random.randint(1, max(2, sides))
        await interaction.response.send_message(f"🎲 You rolled: **{result}** (1-{sides})")
    
    @app_commands.command(name="flip", description="Flip a coin")
    async def flip_coin(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="Coin Flip", description=f"🪙 **{result}**", color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="8ball", description="Ask the magic 8-ball")
    @app_commands.describe(question="Your question")
    async def magic_8ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "Yes definitely", "No way", "Ask again later", "Maybe", "Absolutely",
            "Don't count on it", "Looking good", "Outlook not so good", 
            "Concentrate and ask again", "It is certain", "Very doubtful"
        ]
        embed = discord.Embed(
            title="🔮 Magic 8-Ball",
            description=f"**Q:** {question}\n**A:** {random.choice(responses)}",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="pickaside", description="Pick a random side")
    @app_commands.describe(option_a="First option", option_b="Second option")
    async def pick_a_side(self, interaction: discord.Interaction, option_a: str, option_b: str):
        choice = random.choice([option_a, option_b])
        embed = discord.Embed(
            title="🎯 Picker",
            description=f"I choose: **{choice}**",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="rng", description="Generate a random number")
    @app_commands.describe(min_num="Minimum (default: 1)", max_num="Maximum (default: 100)")
    async def random_number(self, interaction: discord.Interaction, min_num: int = 1, max_num: int = 100):
        if min_num >= max_num:
            await interaction.response.send_message("❌ Min must be less than max", ephemeral=True)
            return
        result = random.randint(min_num, max_num)
        await interaction.response.send_message(f"🎰 **{result}** (between {min_num} and {max_num})")

async def setup(bot):
    await bot.add_cog(FunCommands(bot))
