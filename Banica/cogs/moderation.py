import discord
from discord.ext import commands
import re
from datetime import timedelta


member_role = "member"  # default role for assign/remove commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----- ROLE ASSIGN -----
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def assign(self, ctx, member: discord.Member = None, *, role_name: str = None):
        if member is None:
            member = ctx.author
        if role_name is None:
            role_name = member_role

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            match = re.match(r"<@&(\d+)>", role_name)
            if match:
                role = ctx.guild.get_role(int(match.group(1)))
        if role is None:
            await ctx.send("Role not found.")
            return

        try:
            await member.add_roles(role)
            await ctx.send(f"{role.mention} assigned to {member.mention}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to assign that role.")
        except discord.HTTPException as e:
            await ctx.send(f"Discord API error: {e}")

    @assign.error
    async def assign_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don’t have permission to use this command (Manage Roles required).")

    # ----- ROLE REMOVE -----
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def remove(self, ctx, member: discord.Member = None, *, role_name: str = None):
        if member is None:
            member = ctx.author
        if role_name is None:
            role_name = member_role

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            match = re.match(r"<@&(\d+)>", role_name)
            if match:
                role = ctx.guild.get_role(int(match.group(1)))
        if role is None:
            await ctx.send("Role not found.")
            return

        try:
            await member.remove_roles(role)
            await ctx.send(f"Removed {role.mention} from {member.mention}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to remove that role.")
        except discord.HTTPException as e:
            await ctx.send(f"Something went wrong: {e}")

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don’t have permission to use this command (Manage Roles required).")

    # ----- MUTE -----
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason: str):
        timeout_duration = timedelta(minutes=minutes)
        await member.timeout(timeout_duration, reason=reason)

        embed = discord.Embed(
            title=f"{member.display_name} has been muted",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Duration",
                        value=f"{minutes} minutes", inline=False)
        embed.set_footer(text=f"Muted by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don’t have permission to use this command (Timeout Members required).")

    # ----- UNMUTE -----
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        try:
            await member.timeout(None, reason=reason)
            embed = discord.Embed(
                title=f"{member.display_name} has been unmuted",
                color=discord.Color.green()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Unmuted by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.reply("I don't have permission to unmute that user.")
        except discord.HTTPException as e:
            await ctx.reply(f"Something went wrong while unmuting: {e}")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don’t have permission to use this command (Timeout Members required).")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Usage: `?unmute @user [reason]`")

    # ----- MESSAGE PURGE -----
    @commands.command(name="mpurge")
    @commands.has_permissions(manage_messages=True)
    async def mpurge(self, ctx, amount: int):
        if amount < 1:
            await ctx.reply("Please provide a number greater than 0.")
            return
        if amount > 100:
            await ctx.reply("You can only delete up to 100 messages at once.")
            return

        deleted = await ctx.channel.purge(limit=1 + amount)
        confirmation = await ctx.send(f"Deleted {len(deleted) - 1} messages.")
        await confirmation.delete(delay=3)

    @mpurge.error
    async def mpurge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don’t have permission to use this command (Manage Messages required).")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
