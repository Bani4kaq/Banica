import discord
from discord.ext import commands
import shlex
import random
import asyncio
import re


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx, *, options):
        try:
            parts = shlex.split(options)
        except ValueError:
            await ctx.reply("There was an error parsing your options. Make sure your quotes are balanced!")
            return
        if len(parts) < 2:
            await ctx.reply("Please provide at least two options to choose from!")
            return
        choice = random.choice(parts)
        embed = discord.Embed(
            description=f"``{choice}``", color=discord.Color.green())
        await ctx.reply(embed=embed)

    @commands.command(aliases=['rm'])
    async def reminder(self, ctx, time: str = None, *, text: str = None):
        if time is None:
            await ctx.reply("Please specify a duration (e.g. `10m`, `2h`, or `1d`).")
            return
        if text is None:
            text = "something"

        match = re.match(r"^(\d+)([mhd])$", time.lower())
        if not match:
            await ctx.reply("Invalid time format. Use something like `10m`, `2h`, or `1d`.")
            return
        amount, unit = match.groups()
        amount = int(amount)
        delay = 0
        if unit == "m":
            delay = amount * 60
        elif unit == "h":
            delay = amount * 60 * 60
        elif unit == "d":
            delay = amount * 60 * 60 * 24
        await ctx.send(f"Reminder set for {amount}{unit} about: {text}")
        await asyncio.sleep(delay)
        try:
            await ctx.author.send(f"Hey, you asked me to remind you about: {text}")
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I couldn’t DM you your reminder.")


async def setup(bot):
    await bot.add_cog(Utility(bot))
