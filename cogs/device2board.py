import discord
from discord import Embed, Color
from discord.ext import commands
import aiohttp, asyncio, json
import re

class DeviceToBoard(commands.Cog):
    """Device2Board"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='device2Board', aliases=['d2b'])
    async def device2board(self, ctx, *search_term: str):
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""
        search_term = " ".join(search_term)
        pattern = re.compile("^[a-zA-Z0-9_()&,/ -]*$")
        
        if (not pattern.match(search_term)):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="Illegal characters in search term!"))
            return

        search_term = search_term.lower()

        response = ""
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, 'https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.json', ctx)
            if response is None:
                return

        devices = json.loads(response)

        search_results = [ (device["Codename"], device["Brand names"]) for device in devices if 'Brand names' in device and search_term in device['Brand names'].lower() ]
                
        await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="A board with that name was not found!"))


def setup(bot):
    bot.add_cog(DeviceToBoard(bot))

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