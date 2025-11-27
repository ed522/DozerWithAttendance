import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()

# Sync all commands either to the defined guild or all guilds
@bot.event
async def on_ready():
    guild_id = os.getenv("guild_id")

    # If the guild is in the .env, sync to that guild
    if guild_id:
        guild = discord.Object(id=guild_id)
        await bot.tree.sync(guild=guild)
        print("Syncing to defined guild")
    # Otherwise, sync to all guilds (takes longer)
    else:
        await bot.tree.sync(guild=None)
        print("Syncing to all guilds")

async def load_extensions():
    await bot.load_extension("cogs.ScoringGuide")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_extensions())
    token = os.getenv("token")
    bot.run(token)
