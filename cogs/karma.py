from discord.ext import commands
from discord import Color, Embed, Member
from os.path import abspath, dirname
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

        if action == "take":
            val = -1 * val

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        try:
            # ensure this command name isn't in use (you can have the same command name with arg type true and false)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                "SELECT * FROM karma WHERE user_id = ?;", (member.id,))

            res = c.fetchall()

        finally:
            conn.close()

        if len(res) == 0:
            # this user doesn't have karma yet
            try:
                # ensure this command name isn't in use (you can have the same command name with arg type true and false)
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "INSERT INTO karma (user_id, karma) VALUES (?,?);", (member.id, val,))
                c.execute("INSERT INTO karma_history (user_id, invoker_id, amount, timestamp) VALUES (?,?,?,?)",
                          (member.id, ctx.author.id, val, datetime.now().isoformat()))
                conn.commit()
            finally:
                conn.close()

        else:
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "UPDATE karma SET karma = karma + ? WHERE user_id = ?;", (val, member.id,))
                c.execute("INSERT INTO karma_history (user_id, invoker_id, amount, timestamp) VALUES (?,?,?,?)",
                          (member.id, ctx.author.id, val, datetime.now().isoformat()))
                conn.commit()
            finally:
                conn.close()

        # send success response with current karma
        try:
            # ensure this command name isn't in use (you can have the same command name with arg type true and false)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                "SELECT * FROM karma WHERE user_id = ?;", (member.id,))

            res = c.fetchall()[0][1]
        finally:
            conn.close()

        embed = Embed(title=f"Updated user's karma!",
                      color=Color(value=0x37b83b))
        embed.add_field(name=f'User', value=member.mention)
        embed.add_field(name=f'Invoker', value=ctx.author.mention)
        if val < 0:
            embed.add_field(name=f'Karma taken', value=-1 * val)
        else:
            embed.add_field(name=f'Karma given', value=val)
        embed.add_field(name=f'Current karma', value=res)
        await ctx.send(embed=embed)

        # err handling
    @karma.error
    async def karma_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}\nExample usage: `$karma give @member 3` or `$karma take <ID> 3`'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))
        else:
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))


def setup(bot):
    bot.add_cog(CustomCommands(bot))
