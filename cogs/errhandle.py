import os
import re
import sqlite3
import sys
import traceback
from os.path import abspath, dirname

import discord
from discord import Color, Embed
from discord import AllowedMentions
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            command_name = ctx.invoked_with.lower()
            args = " ".join(ctx.message.content.split(" ",)[1:])
            args_flag = "true" if args != "" else "false"

            BASE_DIR = dirname(dirname(abspath(__file__)))
            db_path = os.path.join(BASE_DIR, "commands.sqlite")
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("SELECT * FROM commands WHERE command_name = ? AND args = ? AND server_id = ?", (command_name, args_flag, ctx.guild.id,))

                data = c.fetchall()
                if (len(data) != 0):
                    c.execute("UPDATE commands SET no_of_uses = ? WHERE command_name = ? AND args = ? AND server_id = ?", (data[0][4]+1, command_name, args_flag, ctx.guild.id,))
                    conn.commit()
                    response = data[0][5]
                    pattern = re.compile(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*")
                    if (pattern.match(response)):
                        response = response + "%20".join(args.split(" "))
                    else:
                        response = response + " " + args
                    await ctx.send(content=response, allowed_mentions=AllowedMentions(everyone=False, users=True, roles=False))
            finally:
                conn.close()
            
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=error))
        elif isinstance(error, commands.BadArgument):

            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')
            # super
       
        elif isinstance(error, commands.NotOwner):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="This command can only be used by the owner of the bot, SlimShadyIAm#9999"))
       
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}').set_footer(text="You should never receive an error like this. Contact SlimShadyIAm#9999."))
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
