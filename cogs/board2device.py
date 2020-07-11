import discord
from discord import Embed, Color
from discord.ext import commands
import aiohttp, asyncio, json

class Board2Device(commands.Cog):
    """Board2Device"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='board2device', aliases=['b2d'])
    async def board2device(self, ctx, board: str):
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""

        if (not board.isalpha()):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="The board should only be alphabetical characters!"))
            return

        board = board.lower()

        response = ""
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, 'https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.json', ctx)
            if response is None:
                return

        response = json.loads(response)
        for device in response:
            if device["Codename"] == board:
                await ctx.send(embed=Embed(title="Board to device results", color=Color(value=0x37b83b), description=f'Board {board} belongs to device {device["Brand names"]}'))
                return
        
        await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="A board with that name was not found!"))


def setup(bot):
    bot.add_cog(Board2Device(bot))

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