import discord
from discord.ext import commands
from discord import app_commands
import os

class NoBlueBanners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nobluebanners", description="🤨")
    async def no_blue_banners(self, interaction: discord.Interaction):
        img_path = os.path.join(os.path.dirname(__file__), "../images/NoBlueBanners.png")
        file = discord.File(img_path, filename="NoBlueBanners.png")
        await interaction.response.send_message(file=file)

async def setup(bot):
    await bot.add_cog(NoBlueBanners(bot))
