import discord
from discord import Embed, Color
from discord.ext import commands
import asyncio
import os

class Utilities(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='timeout')
    @commands.has_permissions(manage_messages=True)
    async def timeout(self, ctx, member: discord.Member=None):
        """Put user on timeout\nExample usage: `$timeout @SlimShadyIAm#9999`"""
        
        if member is None:
            raise commands.BadArgument("Please supply a member, i.e `$timeout @SlimShadyIAm#9999`")
        role = discord.utils.get(ctx.guild.roles, name="timeout")
        if (role is None):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description='timeout role not found!'))
            return
        
        await ctx.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Gave <@{member.id}> the timeout role. We\'ll let them know and remove it in 15 minutes.'))
        embed = Embed(title="You have been put on timeout.", color=Color(value=0xebde34), description=f'{ctx.author.name} gave you the timeout role. We\'ll remove it in 15 minutes.')
        try:
            await member.send(embed=embed)
            await member.add_roles(role)
        except discord.Forbidden:
            channel = discord.utils.get(ctx.guild.channels, name="general" if os.environ.get('PRODUCTION') == "false" else "off-topic")
            await channel.send(f'<@{member.id}> I tried to DM this to you, but your DMs are closed! You\'ll be timed out in 10 seconds.', embed=embed)
            await asyncio.sleep(10)
            await member.add_roles(role)
        
        await asyncio.sleep(900)
        
        embed=Embed(title="Timeout finished.", color=Color(value=0x37b83b), description='Removed your timeout role. Please behave, or we will have to take further action.')
        try:
            await member.send(embed=embed)
            await member.remove_roles(role)
        except discord.Forbidden:
            channel = discord.utils.get(ctx.guild.channels, name="general" if os.environ.get('PRODUCTION') == "false" else "off-topic")
            await channel.send(f'<@{member.id}> I tried to DM this to you, but your DMs are closed!', embed=embed)
            await member.remove_roles(role)
    
        await ctx.author.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Removed {member.name}\'s timeout role.'))

    
    @timeout.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))


def setup(bot):
    bot.add_cog(Utilities(bot))
