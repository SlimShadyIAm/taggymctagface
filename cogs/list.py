from discord.ext import menus
from discord import Embed, Color
from discord.ext import commands
import sqlite3
import random
from os.path import dirname, abspath
import os

class Test:
    def __init__(self, key, value):
        self.key = key
        self.value = value

data = [
    Test(key=key, value=value)
    for key in ['test', 'other', 'okay']
    for value in range(20)
]

class Source(menus.GroupByPageSource):
    async def format_page(self, menu, entry):
        # joined = '\n'.join(f'{i}. <Test value={v.value}>' 
        embed = Embed(title=f'Commands: Page {menu.current_page +1}/{self.get_max_pages()}')
        for i, v in enumerate(entry.items, start=1):
            embed.add_field(name=i, value=v.value)
        # return f'**{entry.key}**\n{joined}\nPage {menu.current_page + 1}/{self.get_max_pages()}'
        return embed

class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='list')
    async def list(self, ctx):
        pages = menus.MenuPages(source=Source(data, key=lambda t: t.key, per_page=12), clear_reactions_after=True)
        await pages.start(ctx)

def setup(bot):
    bot.add_cog(Add(bot))