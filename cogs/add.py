import asyncio
import os
import random
import re
import sqlite3
from os.path import abspath, dirname

from discord import Color, Embed
from discord.ext import commands


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add')
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, command_name: str, args_flag: str, *, response: str):
        """Add a new command to the database\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!`"""

        # ensure command name doesn't have illegal chars
        pattern = re.compile("^[a-zA-Z0-9_-]*$")
        if (not pattern.match(command_name)):
            raise commands.BadArgument(
                "The command name should only be alphanumeric characters with `_` and `-`!\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!")

        # ensure arg flag is valid
        if (not (args_flag == "true" or args_flag == "false")):
            raise commands.BadArgument(
                "Parameter args_flag should be true or false!\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!")

        # always store command name as lowercase for case insensitivity
        command_name = command_name.lower()
        # join response from param array into a string, to store
        # response = format(' '.join(response))

        # ensure user defined a response
        if (response == ""):
            raise commands.BadArgument(
                "You need to include a response!\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!")

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")

        try:
            # ensure this command name isn't in use (you can have the same command name with arg type true and false)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM commands WHERE command_name = ? AND args = ? AND server_id = ?;",
                      (command_name, args_flag, ctx.guild.id,))

            res = c.fetchall()
        finally:
            conn.close()

        # prepare response
        this_id = -1
        while True:
            this_id = gen_id()
            try:
                # ensure this command name isn't in use (you can have the same command name with arg type true and false)
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "SELECT * FROM commands WHERE command_id = ?;", (this_id,))

                test_id = c.fetchall()

                if (len(test_id) == 0):
                    break
            finally:
                conn.close()

        embed = Embed(title=f"Added command!", color=Color(value=0x37b83b))
        embed.add_field(name=f'Command name', value=command_name)
        embed.add_field(name=f'Args supported?', value=args_flag)
        if response != "":
            temp = response[:100] + "..." if len(response) > 100 else response
            embed.add_field(name=f'Response', value=temp)
        embed.set_footer(
            text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)

        # does a command with this name and arg type already exist?
        if len(res) > 0:
            # yes, give the user the option to overwrite the response
            msg = await ctx.send(embed=Embed(title="Command already exists!", color=Color(value=0xebdb34), description="That command already exists! Would you like to overwrite it?"))
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')

            # check for whether user reacted properly
            def check(reaction, user):
                return user == ctx.message.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎')

            # prompt user, wait for reaction (30 second timeout)
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                await msg.edit(embed=Embed(title="Timed out!", color=Color(value=0xEB4634), description=f"Command `${command_name}` will not be added."))
                return
            else:
                await msg.clear_reactions()
                if (str(reaction.emoji) == '👍'):
                    # overwrite command
                    try:
                        conn = sqlite3.connect(db_path)
                        c = conn.cursor()
                        this_id = res[0][0]
                        c.execute("UPDATE commands SET user_who_added = ?, no_of_uses = ?, response = ? WHERE command_id = ?;", (
                            ctx.author.id, 0, response, this_id))
                        conn.commit()
                        embed.add_field(name=f'ID', value=this_id)
                        await msg.edit(embed=embed)
                    finally:
                        conn.close()
                    return
                else:
                    # cancel
                    await msg.edit(embed=Embed(title="Cancelled!", color=Color(value=0xEB4634), description=f"Command `${command_name}` will not be added."))
                    return
            return

        # command name was not in use, add it normally
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            c.execute("INSERT OR REPLACE INTO commands (command_id, server_id, user_who_added, command_name, no_of_uses, response, args) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (this_id, ctx.guild.id, ctx.author.id, command_name, 0, response, args_flag))
            conn.commit()
        finally:
            conn.close()

        # send success response
        embed.add_field(name=f'ID', value=this_id)
        await ctx.send(embed=embed)

    # err handling
    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You\'re fired!`"'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))


def setup(bot):
    bot.add_cog(CustomCommands(bot))


def gen_id():
    return random.randint(0, 10000000)
