import os
import re
import sqlite3
from os.path import abspath, dirname

import discord
from discord import Color, Embed
from discord.ext import commands, menus


class Source(menus.GroupByPageSource):
    async def format_page(self, menu, entry):
        embed = Embed(title=f'Search results: {menu.current_page +1}/{self.get_max_pages()}')
        for v in entry.items:
            res = v[5][:50] + "..." if len(v[5]) > 50 else v[5]
            argo = " [args]" if v[6] == "true" else ""
            if (argo != ""):
                res += argo
            embed.add_field(name=f'${v[3]}{argo}', value=f'**ID**:{v[0]}\n**Supports arguments**:{v[6]}\n**Response**:{res}\n**Creator**:<@{v[2]}>\n**Number of uses**:{v[4]}')
        return embed

class NewMenuPages(menus.MenuPages):
    async def update(self, payload):
        if self._can_remove_reactions:
            if payload.event_type == 'REACTION_ADD':
                await self.bot.http.remove_reaction(
                    payload.channel_id, payload.message_id,
                    discord.Message._emoji_reaction(payload.emoji), payload.member.id
                )
            elif payload.event_type == 'REACTION_REMOVE':
                return
        await super().update(payload)

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
        #send paginated results
        pages = NewMenuPages(source=Source(match, key=lambda t: 1, per_page=6), clear_reactions_after=True)
        await pages.start(ctx)
       
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
