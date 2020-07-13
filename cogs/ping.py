import asyncio
import os
import datetime

import discord
from discord import Color, Embed
from discord.ext import commands


class Utilities(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Pong"""
        now = datetime.datetime.utcnow()
        delta = now - ctx.message.created_at
        await ctx.send(embed=Embed(title="Pong!", color=Color(value=0x37b83b), description=f'The round-trip time is {round(delta.microseconds/1000)}ms').set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url))

def setup(bot):
    bot.add_cog(Utilities(bot))
