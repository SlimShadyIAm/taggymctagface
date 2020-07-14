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
    
    @commands.command(name='search')
    async def search(self, ctx, command_name:str):
        """Add a new command to the database\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You're fired!"""
        
        # ensure command name doesn't have illegal chars
        pattern = re.compile("^[a-zA-Z0-9_-]*$")
        if (not pattern.match(command_name)):
            raise commands.BadArgument("The command name should only be alphanumeric characters with `_` and `-`!\nExample usage:`!search cam-sucks`")
            
        # always store command name as lowercase for case insensitivity
        command_name = command_name.lower()

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        
        try:
            # get list of all commands from this server
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM commands WHERE server_id = ?;", (ctx.guild.id,))
            
            res = c.fetchall()
        finally:
            conn.close()

        match = [ command for command in res if command_name in command[3] ]

        if len(match) == 0:
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'No commands found with that name!'))
            return
        
        embed = Embed(title=f"Search results:", color=Color(value=0x37b83b))
        for command in match:
            #prepare response 
            res = command[5][:50] + "..." if len(command[5]) > 50 else command[5]
            argo = " [args]" if command[6] == "true" else ""
            if (argo != ""):
                res += argo
            embed.add_field(name=f'${command[3]}{argo}', value=f'**ID**:{command[0]}\n**Supports arguments**:{command[6]}\n**Response**:{res}\n**Creator**:<@{command[2]}>\n**Number of uses**:{command[4]}')
            embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            
        # send success response
        await ctx.send(embed=embed)

    #err handling
    @search.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}\nExample usage:`!add cam-sucks false yeah he does` or `!add fire true You\'re fired!`"'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        else:
            print(error)
def setup(bot):
    bot.add_cog(CustomCommands(bot))
