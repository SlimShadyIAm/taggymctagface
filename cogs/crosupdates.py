import discord
from discord import Embed, Color
from discord.ext import commands
import urllib.request, json 

class CrosUpdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="updates")
    @commands.guild_only()
    async def updates(self, ctx, *, board:str=""):
        board = board.lower()
         
        if (board == ''):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You need to supply a board name! Example: `$updates coral`"))
            return
        
        if (not board.isalpha()):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="The board should only be alphabetical characters!"))
            return

        with urllib.request.urlopen("https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.json") as response:
            data = json.load(response)
            
            for data_board in data:
                if data_board['Codename'] == board:
                    # pp.pprint(data_board)
                    embed = Embed(title=f"ChromeOS update status for {board}", color=Color(value=0x37b83b))
                    version = data_board["Stable"].split("<br>")
                    embed.add_field(name=f'Stable Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                    
                    version = data_board["Beta"].split("<br>")
                    embed.add_field(name=f'Beta Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                    
                    version = data_board["Dev"].split("<br>")
                    embed.add_field(name=f'Dev Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                    
                    version = data_board["Canary"].split("<br>")
                    embed.add_field(name=f'Canary Channel', value=f'**Version**: {version[1]}\n**Platform**: {version[0]}')
                    
                    embed.set_footer(text="Powered by https://cros.tech/ (by Skylar)")
                    await ctx.send(embed=embed)
                    return

            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="Couldn't find a result with that boardname!"))
            return

def setup(bot):
    bot.add_cog(CrosUpdates(bot))