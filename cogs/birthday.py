import discord
from discord import Embed, Color
from discord.ext import commands
import asyncio
import os


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='birthday')
    @commands.has_permissions(administrator=True)
    async def birthday(self, ctx, member: discord.Member = None):
        """Give a user the birthday role for 24 hours\nExample usage: `$birthday @SlimShadyIAm#9999`"""

        # ensure user passed in argument
        if member is None:
            raise commands.BadArgument(
                "Please supply a member, i.e `$birthday @SlimShadyIAm#9999`")

        # grab birthday role object
        role = discord.utils.get(ctx.guild.roles, name="birthday boi")
        # throw error if no birthday role in server
        if (role is None):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description='birthday boi role not found!'))
            return

        # give user role
        await member.add_roles(role)
        await ctx.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Gave <@{member.id}> the birthday role. We\'ll let them know and remove it in 24 hours.').set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url))

        # dm the user to notify them...
        embed = Embed(title="Happy birthday!  🥳", color=Color(value=0xebde34), description=f'{ctx.author.name} gave you the birthday role. We\'ll remove it in 24 hours.').set_footer(
            text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        try:
            # try to dm them
            await member.send(embed=embed)
        except discord.Forbidden:
            # the user's dm's are closed, so we send it to the main server instead
            channel = discord.utils.get(ctx.guild.channels, name="general" if os.environ.get(
                'PRODUCTION') == "false" else "off-topic")
            await channel.send(f'<@{member.id}> I tried to DM this to you, but your DMs are closed!', embed=embed)

        # wait 24 hours
        await asyncio.sleep(86400)
        # remove role
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="birthday boi"))

        # again try to dm user to notify them
        embed = Embed(title="Party's over.", color=Color(value=0x37b83b), description='Removed your birthday role.').set_footer(
            text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            channel = discord.utils.get(ctx.guild.channels, name="general" if os.environ.get(
                'PRODUCTION') == "false" else "off-topic")
            await channel.send(f'<@{member.id}> I tried to DM this to you, but your DMs are closed!', embed=embed)

        # let the admin who gave the role know
        await ctx.author.send(embed=Embed(title="Done!", color=Color(value=0x37b83b), description=f'Removed {member.name}\'s birthday role.'))

    # err handling
    @birthday.error
    async def birthday_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))


def setup(bot):
    bot.add_cog(Utilities(bot))
