import discord
from discord import Embed, Color
from discord.ext import commands
import asyncio

pingUsers = []

class Utilities(commands.Cog):
    """Helpers"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='helpers')
    async def helpers(self, ctx):
        """Tag helpers, usable in #support once every 24 hours per user"""
        print()
        if (ctx.channel.name != "support"):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'This command is only usable in <#{discord.utils.get(ctx.guild.channels, name="support").id}>!'))
            return
        if ctx.author in pingUsers:
            await ctx.send(embed=Embed(title="Cooldown", color=Color(value=0xEB4634), description="You can only use this command once every 24 hours."))
            return 

        await ctx.send(f'<@{ctx.author.id}> pinged <@&{discord.utils.get(ctx.guild.roles, name="Helpers").id}>')
        pingUsers.append(ctx.author)
        await asyncio.sleep(86400)
        pingUsers.remove(ctx.author)

def setup(bot):
    bot.add_cog(Utilities(bot))
