import asyncio
import json

import aiohttp
import discord
from discord import Color, Embed
from discord.ext import commands

class Utilities(commands.Cog):
    """Board2Device"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='board2device', aliases=['b2d'])
    async def board2device(self, ctx, board: str):
        """(alias $b2d) Retreive the brand name for a given Chromebook board name\nExample usage: `$b2d edgar`"""

        if (not board.isalpha()):
            raise commands.BadArgument()

        board = board.lower()

        response = ""
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, 'https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.json', ctx)
            if response is None:
                return

        response = json.loads(response)
        for device in response:
            if device["Codename"] == board:
                await ctx.send(embed=Embed(title=f'{device["Codename"]} belongs to...', color=Color(value=0x37b83b), description=device["Brand names"]))
                return
        
        await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="A board with that name was not found!"))

    @board2device.error
    async def b2d_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You need to supply a board name! Example: `$b2d coral`"))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="The board should only be alphabetical characters!"))

def setup(bot):
    bot.add_cog(Utilities(bot))

async def fetch(session, url, ctx):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="Error connecting to the feed! Please try again later"))
                return None
    except aiohttp.ClientConnectionError:
        await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="Error connecting to the feed! Please try again later"))
        return None
