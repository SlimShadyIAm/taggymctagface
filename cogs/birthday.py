import discord
from discord import Embed, Color
from discord.ext import commands
import asyncio

class Birthday(commands.Cog):
    """Birthday"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='birthday')
    @commands.has_role("Admin")
    async def birthday(self, ctx, member: discord.Member = None):
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""

        if member is None:
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="Please supply a member, i.e `$birthday @SlimShadyIAm#9999`"))
            return

        await member.add_roles(discord.utils.get(ctx.guild.roles, name="Birthday boi"))
        await ctx.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Gave <@{member.id}> the birthday role. We\'ll let them know and remove it in 24 hours.'))
        await member.send(embed=Embed(title="Happy birthday!  🥳", color=Color(value=0xebde34), description=f'{ctx.author.name} gave you the birthday role. We\'ll remove it in 24 hours.'))
        await asyncio.sleep(86400)
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Birthday boi"))
        await ctx.author.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Removed {member.name}\'s birthday role.'))
        await member.send(embed=Embed(title="Party's over.", color=Color(value=0x37b83b), description='Removed your birthday role.'))
def setup(bot):
    bot.add_cog(Birthday(bot))
