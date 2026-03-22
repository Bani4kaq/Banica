import discord
from discord.ext import commands
import os

LOG_CHANNEL_NAME = os.getenv("LOG_CHANNEL_NAME", "audit-log")


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild):
        """Helper to find the log channel or None."""
        return discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)

    # ----- MESSAGE EVENTS -----
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.author.bot:
            return
        log_channel = await self.get_log_channel(message.guild)
        if not log_channel:
            return
        embed = discord.Embed(title="Message Deleted",
                              color=discord.Color.red())
        embed.add_field(
            name="Author", value=f"{message.author} ({message.author.id})", inline=False)
        embed.add_field(
            name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(
            name="Content", value=message.content or "*[no text]*", inline=False)
        if message.attachments:
            embed.add_field(name="Attachments", value="\n".join(
                a.url for a in message.attachments), inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild or before.author.bot or before.content == after.content:
            return
        log_channel = await self.get_log_channel(before.guild)
        if not log_channel:
            return
        embed = discord.Embed(title="Message Edited",
                              color=discord.Color.orange())
        embed.add_field(
            name="Author", value=f"{before.author} ({before.author.id})", inline=False)
        embed.add_field(
            name="Channel", value=before.channel.mention, inline=False)
        embed.add_field(
            name="Before", value=before.content or "*[no text]*", inline=False)
        embed.add_field(
            name="After", value=after.content or "*[no text]*", inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        log_channel = await self.get_log_channel(channel.guild)
        if not log_channel:
            return
        embed = discord.Embed(title="Pins Updated", color=discord.Color.gold())
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Last Pin Time",
                        value=str(last_pin), inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)

    # ----- MEMBER EVENTS -----
    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = await self.get_log_channel(member.guild)
        if log_channel:
            embed = discord.Embed(title="Member Joined",
                                  color=discord.Color.green())
            embed.add_field(
                name="User", value=f"{member} ({member.id})", inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = await self.get_log_channel(member.guild)
        if log_channel:
            embed = discord.Embed(title="Member Left",
                                  color=discord.Color.red())
            embed.add_field(
                name="User", value=f"{member} ({member.id})", inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            embed = discord.Embed(title="User Banned",
                                  color=discord.Color.dark_red())
            embed.add_field(
                name="User", value=f"{user} ({user.id})", inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            embed = discord.Embed(title="User Unbanned",
                                  color=discord.Color.green())
            embed.add_field(
                name="User", value=f"{user} ({user.id})", inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.guild:
            return
        log_channel = await self.get_log_channel(before.guild)
        if not log_channel:
            return

        # Track timeout changes
        before_timeout = before.timed_out_until
        after_timeout = after.timed_out_until
        if before_timeout != after_timeout:
            embed = discord.Embed(
                title="Member Timeout Updated", color=discord.Color.dark_orange())
            embed.add_field(
                name="User", value=f"{after} ({after.id})", inline=False)
            if after_timeout is None:
                embed.add_field(
                    name="Action", value="Timeout removed", inline=False)
            else:
                embed.add_field(name="Action", value="Timed out", inline=False)
                embed.add_field(name="Until", value=str(
                    after_timeout), inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    # ----- CHANNEL EVENTS -----
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = await self.get_log_channel(channel.guild)
        if log_channel:
            embed = discord.Embed(title="Channel Created",
                                  color=discord.Color.green())
            embed.add_field(name="Channel", value=channel.name, inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = await self.get_log_channel(channel.guild)
        if log_channel:
            embed = discord.Embed(title="Channel Deleted",
                                  color=discord.Color.red())
            embed.add_field(name="Channel", value=channel.name, inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    # ----- ROLE EVENTS -----
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        log_channel = await self.get_log_channel(role.guild)
        if log_channel:
            embed = discord.Embed(title="Role Created",
                                  color=discord.Color.green())
            embed.add_field(name="Role", value=role.name, inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel = await self.get_log_channel(role.guild)
        if log_channel:
            embed = discord.Embed(title="Role Deleted",
                                  color=discord.Color.red())
            embed.add_field(name="Role", value=role.name, inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)

    # ----- EMOJI EVENTS -----
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            embed = discord.Embed(title="Emojis Updated",
                                  color=discord.Color.blurple())
            embed.add_field(name="Before", value=", ".join(
                e.name for e in before) or "None", inline=False)
            embed.add_field(name="After", value=", ".join(
                e.name for e in after) or "None", inline=False)
            embed.timestamp = discord.utils.utcnow()
            await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logging(bot))
