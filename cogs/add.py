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
    async def add(self, ctx, command_name:str, args_flag:str, *, response:str):
        """Add a new command to the database\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!"""
        
        # ensure command name doesn't have illegal chars
        pattern = re.compile("^[a-zA-Z0-9_-]*$")
        if (not pattern.match(command_name)):
            raise commands.BadArgument("The command name should only be alphanumeric characters with `_` and `-`!\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!")

        # ensure arg flag is valid
        if (not (args_flag == "true" or args_flag == "false")):
            raise commands.BadArgument("Parameter args_flag should be true or false!\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!")
            
        # always store command name as lowercase for case insensitivity
        command_name = command_name.lower()
        # join response from param array into a string, to store
        # response = format(' '.join(response))
        
        # ensure user defined a response
        if (response == ""):
            raise commands.BadArgument("You need to include a response!\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!")

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        
        try:
            # ensure this command name isn't in use (you can have the same command name with arg type true and false)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM commands WHERE command_name = ? AND args = ? AND server_id = ?;", (command_name, args_flag, ctx.guild.id,))
            
            res = c.fetchall()
            # command name in use
            if len(res) > 0:
                await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="That command already exists!"))
                return
            
            # yay this isn't in use, store it
            this_id = gen_id()
            c.execute("INSERT OR REPLACE INTO commands (command_id, server_id, user_who_added, command_name, no_of_uses, response, args) VALUES (?, ?, ?, ?, ?, ?, ?)", (this_id, ctx.guild.id, ctx.author.id, command_name, 0, response, args_flag ))
            conn.commit()
        finally:
            conn.close()
        
        # send success response
        embed = embed=Embed(title=f"Added command!", color=Color(value=0x37b83b))
        embed.add_field(name=f'Command name', value=command_name)
        embed.add_field(name=f'Args supported?', value=args_flag)
        embed.add_field(name=f'ID', value=this_id)
        if response != "":
            response = response[:100] + "..." if len(response) > 100 else response
            embed.add_field(name=f'Response', value=response)
        await ctx.send(embed=embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url))

    #err handling
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
