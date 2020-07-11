from discord.ext import menus
from discord import Embed, Color
from discord.ext import commands
import sqlite3
import random
from os.path import dirname, abspath
import os

class Source(menus.GroupByPageSource):
    async def format_page(self, menu, entry):
        embed = Embed(title=f'Commands: Page {menu.current_page +1}/{self.get_max_pages()}')
        print (entry)
        for i, v in enumerate(entry.items, start=1):
            res = f'\n**Response**:{v[5]}' if v[6] == 'true' else ''
            embed.add_field(name=f'${v[3]}', value=f'**ID**:{v[0]}\n**Supports arguments**:{v[6]}{res}\n**Creator**:<@{v[2]}>\n**Number of uses**:{v[4]}')
        return embed

class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='list')
    async def list(self, ctx):
        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM commands WHERE server_id = ? ORDER BY command_name", (253908290105376768,))

        data = c.fetchall()
        conn.close()
        if (len(data) == 0) {
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="No commands in this guild!"))
        } else {
            pages = menus.MenuPages(source=Source(data, key=lambda t: t[0], per_page=6), clear_reactions_after=True)
            await pages.start(ctx)
        }

def setup(bot):
    bot.add_cog(Add(bot))