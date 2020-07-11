import os
import random
import re
import sqlite3
from os.path import abspath, dirname

from discord import Color, Embed
from discord.ext import commands


class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='add')
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, command_name:str, args:str, *rest):
        pattern = re.compile("^[a-zA-Z0-9_-]*$")
        if (not pattern.match(command_name)):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="The command name should only be alphabetical characters!"))
            return
        
        if (not (args == "true" or args == "false")):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="Parameter args should be true or false!"))
            return
        
        rest = format(' '.join(rest))
        
        if (rest == ""):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You need to include a response!"))
            return
        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM commands WHERE command_name = ? AND args = ?;", (command_name, args,))
            
            res = c.fetchall()
            if len(res) > 0:
                await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="That command already exists!"))
                return
            this_id = gen_id()
            c.execute("INSERT OR REPLACE INTO commands (command_id, server_id, user_who_added, command_name, no_of_uses, response, args) VALUES (?, ?, ?, ?, ?, ?, ?)", (this_id, ctx.guild.id, ctx.author.id, command_name, 0, rest, args ))
            conn.commit()
        finally:
            conn.close()
        
        embed = embed=Embed(title=f"Added command!", color=Color(value=0x37b83b))
        embed.add_field(name=f'Command name', value=command_name)
        embed.add_field(name=f'Args supported?', value=args)
        embed.add_field(name=f'ID', value=this_id)
        if rest != "":
            embed.add_field(name=f'Response', value=rest)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Add(bot))

def gen_id():
    return random.randint(0, 10000000)
