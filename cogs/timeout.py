import discord
from discord import Embed, Color
from discord.ext import commands
import asyncio

class Utilities(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='timeout')
    @commands.has_permissions(manage_messages=True)
    async def timeout(self, ctx, member: discord.Member=None):
        """Put user on timeout"""

        if member is None:
            raise commands.BadArgument("Please supply a member, i.e `$timeout @SlimShadyIAm#9999`")
        role = discord.utils.get(ctx.guild.roles, name="timeout")
        if (role is None):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description='timeout role not found!'))
            return;
        await member.add_roles(role)
        await ctx.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Gave <@{member.id}> the timeout role. We\'ll let them know and remove it in 15 minutes.'))
        await member.send(embed=Embed(title="You have been put on timeout.", color=Color(value=0xebde34), description=f'{ctx.author.name} gave you the timeout role. We\'ll remove it in 15 minutes.'))
        await asyncio.sleep(900)
        await member.remove_roles(role)
        await ctx.author.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Removed {member.name}\'s timeout role.'))
        await member.send(embed=Embed(title="Timeout finished.", color=Color(value=0x37b83b), description='Removed your timeout role. Please behave, or we will have to take further action.'))
    
    @timeout.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))


def setup(bot):
    bot.add_cog(Utilities(bot))
