from discord.ext import menus
from discord import Embed, Color
import discord
from discord.ext import commands
import sqlite3
import random
from os.path import dirname, abspath
import os

class Source(menus.GroupByPageSource):
    async def format_page(self, menu, entry):
        embed = Embed(title=f'Commands: Page {menu.current_page +1}/{self.get_max_pages()}')
        for v in entry.items:
            embed.add_field(name=f'${v[3]}', value=f'**ID**:{v[0]}\n**Supports arguments**:{v[6]}\n**Response**:{v[5]}\n**Creator**:<@{v[2]}>\n**Number of uses**:{v[4]}')
        return embed

class NewMenuPages(menus.MenuPages):
    async def update(self, payload):
        if self._can_remove_reactions:
            if payload.event_type == 'REACTION_ADD':
                await self.bot.http.remove_reaction(
                    payload.channel_id, payload.message_id,
                    discord.Message._emoji_reaction(payload.emoji), payload.member.id
                )
            elif payload.event_type == 'REACTION_REMOVE':
                return
        await super().update(payload)
        
class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='list', aliases=["ls"])
    async def list(self, ctx):
        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM commands WHERE server_id = ? ORDER BY command_name", (ctx.guild.id,))
            # c.execute("SELECT * FROM commands WHERE server_id = ? ORDER BY command_name", (253908290105376768 if os.environ.get('PRODUCTION') == "false" else ctx.guild.id,))

            data = c.fetchall()
            if (len(data) == 0):
                await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="No commands in this guild!"))
            else:
                pages = NewMenuPages(source=Source(data, key=lambda t: 1, per_page=6), clear_reactions_after=True)
                await pages.start(ctx)
        finally:
            conn.close()
def setup(bot):
    bot.add_cog(Add(bot))