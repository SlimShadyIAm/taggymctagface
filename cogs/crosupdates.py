import discord
from discord import Embed, Color
from discord.ext import commands
import aiohttp, asyncio, json
import traceback

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cros-updates", aliases=['updates'])
    @commands.guild_only()
    async def updates(self, ctx, *, board:str):
        """(alias $updates) Get ChromeOS version data for a specified Chromebook board name\nExample usage: `$updates edgar`"""
        # ensure the board arg is only alphabetical chars
        if (not board.isalpha()):
            raise commands.BadArgument()

        # case insensitivity
        board = board.lower()

        # fetch data from skylar's API
        data = ""
        async with aiohttp.ClientSession() as session:
            data = await fetch(session, 'https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.json', ctx)
            if data is None:
                return
        
        #parse response to json
        data = json.loads(data)
        # loop through response to find board
        for data_board in data:
            # did we find a match
            if data_board['Codename'] == board:
                # yes, send the data
                embed = Embed(title=f"ChromeOS update status for {board}", color=Color(value=0x37b83b))
                version = data_board["Stable"].split("<br>")
                embed.add_field(name=f'Stable Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                
                version = data_board["Beta"].split("<br>")
                if len(version) == 2:
                    embed.add_field(name=f'Beta Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                else:
                    embed.add_field(name=f'Beta Channel', value=f'**Version**: {data_board["Beta"]}')
                
                version = data_board["Dev"].split("<br>")
                if len(version) == 2:
                    embed.add_field(name=f'Dev Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                else:
                    embed.add_field(name=f'Dev Channel', value=f'**Version**: {data["Dev"]}')
                
                if (data_board["Canary"] is not None):
                    version = data_board["Canary"].split("<br>")
                    if len(version) == 2:
                        embed.add_field(name=f'Canary Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                
                embed.set_footer(text=f"Powered by https://cros.tech/ (by Skylar), requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return

        # board not found, error
        await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="Couldn't find a result with that boardname!"))
        return

    # err handling
    @updates.error
    async def updates_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You need to supply a board name! Example: `$updates coral`"))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="The board should only be alphabetical characters!"))
        else:
            await ctx.send(embed=Embed(title="A fatal error occured!", color=Color(value=0xEB4634), description="Tell slim :("))
            traceback.print_exc()

def setup(bot):
    bot.add_cog(Utilities(bot))

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