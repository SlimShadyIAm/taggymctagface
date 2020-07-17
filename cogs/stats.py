import discord
from discord import Color, Embed
from discord.ext import commands
import sys
import traceback
import platform
import psutil
import time
import datetime

start_time = time.time()


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats")
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def stats(self, ctx, cog=None):
        """Get bot stats"""
        guilds = len(self.bot.guilds)
        channels = sum([len(guild.channels) for guild in self.bot.guilds])
        users = sum([len(guild.members) for guild in self.bot.guilds])

        embed = discord.Embed(
            title=f"{self.bot.user.name} Statistics", color=Color(value=0xae52ff))
        embed.add_field(name="Bot Version", value=discord.__version__)
        embed.add_field(name="Uptime", value=await self.uptime())

        embed.add_field(name="Servers", value=str(guilds))
        embed.add_field(name="Channels", value=str(channels))
        embed.add_field(name="Users", value=str(users))
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="RAM Usage",
                        value=f"{round(psutil.virtual_memory().used / 1000000)} MB / {round(psutil.virtual_memory().total / 1000000)} MB")
        embed.add_field(name="Python Version", value=platform.python_version())
        embed.add_field(name="discord.py Version", value=discord.__version__)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(
            text=f"Made with ❤ by SlimShadyIAm#9999", icon_url="https://images-ext-2.discordapp.net/external/2QAqIY9YknSzgB1z1GljSqojuOAbYKu9XvXLiMDD5EM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/109705860275539968/a_8c51d609d3759ebf706dc9809ccd6a44.gif",
        )
        await ctx.send(embed=embed)

    async def uptime(self):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        return text

    @ stats.error
    async def stats_error(self, ctx, error):
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
    bot.add_cog(Admin(bot))
