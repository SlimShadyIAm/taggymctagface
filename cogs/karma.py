import discord
from discord.ext import commands
from discord import Color, Embed, Member
from os.path import abspath, dirname
import sys
import traceback
import sqlite3
import asyncio
import os
from datetime import datetime


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='karma')
    @commands.has_permissions(manage_messages=True)
    async def karma(self, ctx, action: str, member: Member, val: int):
        """Give or take karma from a user.\nYou may give or take up to 3 karma in a single command.\nExample usage: `$karma give @member 3` or `$karma take <ID> 3`"""

        action = action.lower()
        if action != "give" and action != "take":
            raise commands.BadArgument(
                "The action should be either \"give\" or \"take\"\nExample usage: `$karma give @member 3` or `$karma take <ID> 3`")

        if val < 1 or val > 3:
            raise commands.BadArgument(
                "You can give or take 1-3 karma in a command!\nExample usage: `$karma give @member 3` or `$karma take <ID> 3`")

        if member.bot:
            raise commands.BadArgument(
                "You can't give a bot karma")

        if member.id == ctx.author.id and member.id != self.bot.owner_id:
            raise commands.BadArgument(
                "You can't give yourself karma")

        if action == "take":
            val = -1 * val

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                "SELECT * FROM karma WHERE user_id = ? AND guild_id = ?;", (member.id, ctx.guild.id,))

            res = c.fetchall()

        finally:
            conn.close()

        if len(res) == 0:
            # this user doesn't have karma yet
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "INSERT INTO karma (user_id, guild_id, karma) VALUES (?,?,?);", (member.id, ctx.guild.id, val))
                c.execute("INSERT INTO karma_history (guild_id, user_id, invoker_id, amount, timestamp) VALUES (?,?,?,?,?)",
                          (ctx.guild.id, member.id, ctx.author.id, val, datetime.now().isoformat()))
                c.execute("INSERT OR REPLACE INTO users (user_id, nickname) VALUES(?,?)",
                          (member.id, f'{member.name}#{member.discriminator}',))
                c.execute("INSERT OR REPLACE INTO users (user_id, nickname) VALUES(?,?)",
                          (ctx.author.id, f'{ctx.author.name}#{ctx.author.discriminator}',))
                conn.commit()
            finally:
                conn.close()

        else:
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "UPDATE karma SET karma = karma + ? WHERE user_id = ? AND guild_id = ?;", (val, member.id, ctx.guild.id,))
                c.execute("INSERT INTO karma_history (guild_id,user_id, invoker_id, amount, timestamp) VALUES (?,?,?,?,?)",
                          (ctx.guild.id, member.id, ctx.author.id, val, datetime.now().isoformat()))
                c.execute("INSERT OR REPLACE INTO users (user_id, nickname) VALUES(?,?)",
                          (member.id, f'{member.name}#{member.discriminator}',))
                c.execute("INSERT OR REPLACE INTO users (user_id, nickname) VALUES(?,?)",
                          (ctx.author.id, f'{ctx.author.name}#{ctx.author.discriminator}',))
                conn.commit()
            finally:
                conn.close()

        # send success response with current karma
        try:
            # ensure this command name isn't in use (you can have the same command name with arg type true and false)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                "SELECT karma, rank, notified_good, notified_bad FROM ( SELECT karma, user_id, notified_good, notified_bad, RANK() OVER ( ORDER BY karma DESC ) rank FROM karma WHERE guild_id = ?) WHERE user_id = ?;", (ctx.guild.id, member.id,))

            res = c.fetchall()[0]
        finally:
            conn.close()

        embed = Embed(title=f"Updated {member.name}#{member.discriminator}'s karma!",
                      color=Color(value=0x37b83b))
        embed.description = ""
        if val < 0:
            embed.description += f'**Karma taken**: {-1 * val}\n'
        else:
            embed.description += f'**Karma given**: {val}\n'
        embed.description += f'**Current karma**: {res[0]}\n'
        embed.description += f'**Leaderboard rank**: {res[1]}'
        embed.set_footer(
            text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        if res[2] == 0 and res[0] > 50:
            channel = discord.utils.get(ctx.guild.channels, name="bot-test" if os.environ.get(
                'PRODUCTION') == "false" else "nerds")
            role = discord.utils.get(ctx.guild.roles, name="bot tester" if os.environ.get(
                'PRODUCTION') == "false" else "Moderators")
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "UPDATE karma SET notified_good = 1 WHERE user_id = ? AND guild_id = ?;", (member.id, ctx.guild.id,))
                conn.commit()
            finally:
                conn.close()
            await channel.send(f"{role.mention} {member.mention} has karma over 50! Consider making him a nerd.")
        elif res[3] == 0 and res[0] < -20:
            channel = discord.utils.get(ctx.guild.channels, name="bot-test" if os.environ.get(
                'PRODUCTION') == "false" else "nerds")
            role = discord.utils.get(ctx.guild.roles, name="bot tester" if os.environ.get(
                'PRODUCTION') == "false" else "Moderators")
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "UPDATE karma SET notified_bad = 1 WHERE user_id = ? AND guild_id = ?;", (member.id, ctx.guild.id,))
                conn.commit()
            finally:
                conn.close()
            await channel.send(f"{role.mention} {member.mention} has karma under -20! Consider disciplining him.")

    # err handling
    @ karma.error
    async def karma_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}\nExample usage: `$karma give @member 3` or `$karma take <ID> 3`'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))
        else:
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CustomCommands(bot))
