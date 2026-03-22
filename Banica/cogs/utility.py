import discord
from discord.ext import commands
import asyncio
import shlex
import random
import re
from datetime import timedelta


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----- CHOOSE COMMAND -----
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
            description=f"``{choice}``",
            color=discord.Color.green()
        )
        await ctx.reply(embed=embed)

    # ----- REMINDER COMMAND -----
    @commands.command(aliases=['rm'])
    async def reminder(self, ctx, time: str = None, *, text: str = None):
        if time is None:
            await ctx.reply("Please specify a duration (e.g. `?rm 10m`, `?rm 2h`, or `?rm 1d`).")
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
        unit_full = ""

        if unit == "m":
            delay = amount * 60
            unit_full = "minute" if amount == 1 else "minutes"
        elif unit == "h":
            delay = amount * 60 * 60
            unit_full = "hour" if amount == 1 else "hours"
        elif unit == "d":
            delay = amount * 60 * 60 * 24
            unit_full = "day" if amount == 1 else "days"
        else:
            await ctx.reply("Invalid time unit. Use m, h, or d.")
            return

        embed = discord.Embed(
            title="Reminder Set",
            description=f"{ctx.author.mention}, I will remind you in **{amount} {unit_full}** about **{text}**.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Reminder bot")
        await ctx.send(embed=embed)

        await asyncio.sleep(delay)

        try:
            await ctx.author.send(f"Hey, you asked me to remind you about {text}.")
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I couldn’t DM you your reminder (your DMs might be closed).")


async def setup(bot):
    await bot.add_cog(Utility(bot))
