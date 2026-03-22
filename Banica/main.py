import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv
import asyncio

# ----- ENVIRONMENT -----
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ----- LOGGING -----
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO, handlers=[handler])

# ----- INTENTS -----
intents = discord.Intents.all()

# ----- BOT INSTANCE -----
bot = commands.Bot(command_prefix='?', intents=intents)

# ----- ON READY -----


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}!")

# ----- AUTOMATIC COG LOADING -----


async def load_cogs():
    cogs = ["cogs.logging", "cogs.vc",
            "cogs.moderation"]  # add other cogs here
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"Loaded cog: {cog}")
        except commands.ExtensionNotFound:
            print(f"Cog not found: {cog}")
        except commands.ExtensionAlreadyLoaded:
            print(f"Cog already loaded: {cog}")
        except commands.NoEntryPointError:
            print(f"Cog missing setup(): {cog}")
        except commands.ExtensionFailed as e:
            print(f"Error loading {cog}: {e.__class__.__name__}: {e}")

# ----- STARTUP -----


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

# ----- RUN -----
asyncio.run(main())
