import discord
from discord import Embed, Color
from discord.ext import commands
import aiohttp, asyncio, json

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cros-updates", aliases=['updates'])
    @commands.guild_only()
    async def updates(self, ctx, *, board:str=""):
        board = board.lower()
         
        if (board == ''):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You need to supply a board name! Example: `$updates coral`"))
            return
        
        if (not board.isalpha()):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="The board should only be alphabetical characters!"))
            return

        data = ""
        async with aiohttp.ClientSession() as session:
            data = await fetch(session, 'https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.json', ctx)
            if data is None:
                return
                
        data = json.loads(data)
        for data_board in data:
            if data_board['Codename'] == board:
                embed = Embed(title=f"ChromeOS update status for {board}", color=Color(value=0x37b83b))
                version = data_board["Stable"].split("<br>")
                embed.add_field(name=f'Stable Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                
                version = data_board["Beta"].split("<br>")
                embed.add_field(name=f'Beta Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                
                version = data_board["Dev"].split("<br>")
                embed.add_field(name=f'Dev Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                
                if (data_board["Canary"] is not None):
                    version = data_board["Canary"].split("<br>")
                    if len(version) == 2:
                        embed.add_field(name=f'Canary Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                
                embed.set_footer(text="Powered by https://cros.tech/ (by Skylar)")
                await ctx.send(embed=embed)
                return

        await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="Couldn't find a result with that boardname!"))
        return

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