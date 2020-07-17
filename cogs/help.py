import discord
from discord import Color, Embed
from discord.ext import commands
import sys
import traceback


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help_comm(self, ctx, cog=None):
        """Gets all cogs and commands of mine."""
        if not cog:
            """Cog listing.  What more?"""
            halp = discord.Embed(title='All commands', color=Color(value=0x3f78eb),
                                 description='Use `.help commandname` to find out more about a command!')
            for cogs in self.bot.commands:
                if not cogs.hidden:
                    halp.add_field(name=f'{self.bot.command_prefix}{cogs.name}', value=cogs.help.split(
                        "\n")[0], inline=False)
            await ctx.send(embed=halp)
        else:
            for cogs in self.bot.commands:
                if cogs.name == cog and not cogs.hidden:
                    halp = discord.Embed(title=f'Help results for {self.bot.command_prefix}{cogs.name}', color=Color(value=0x3f78eb),
                                         description=cogs.help)
                    await ctx.send(embed=halp)
                    return
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description='Command not found'))

    @help_comm.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error} If you are trying to use a role with spaces, put the name in quotes or mention it (`@role name`).'))
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}. See `.help subscribe` if you need help.'))
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You need `MANAGE_SERVER` permission to run this command."))
            return
        else:
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}. Send a screenshot of this error to SlimShadyIAm#9999'))
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)
            return


def setup(bot):
    bot.add_cog(Utilities(bot))
