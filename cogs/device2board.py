import asyncio
import json
import re

import aiohttp
import discord
from discord import Color, Embed
from discord.ext import commands, menus


class Utilities(commands.Cog):
    """Device2Board"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='device2board', aliases=['d2b'])
    async def device2board(self, ctx, *, search_term: str):
        """(alias $d2b) Retrieve the board name from a specified brand name as a search term\nExample usage: `$d2b acer chromebook 11`"""

        if search_term == "":
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You need to supply a boardname! Example: `$d2b acer chromebook`"))
            return
        pattern = re.compile("^[a-zA-Z0-9_()&,/ -]*$")

        if (not pattern.match(search_term)):
            raise commands.BadArgument("Illegal characters in search term!")

        search_term = search_term.lower()

        response = ""
        async with aiohttp.ClientSession() as session:
            response = await fetch(session, 'https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.json', ctx)
            if response is None:
                return

        devices = json.loads(response)

        search_results = [(device["Codename"], device["Brand names"])
                          for device in devices if 'Brand names' in device and search_term in device['Brand names'].lower()]
        if len(search_results) == 0:
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="A board with that name was not found!"))
        else:
            pages = NewMenuPages(source=Source(
                search_results, key=lambda t: 1, per_page=8), clear_reactions_after=True)
            await pages.start(ctx)

    @device2board.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))


class Source(menus.GroupByPageSource):
    async def format_page(self, menu, entry):
        embed = Embed(
            title=f'Search results: Page {menu.current_page +1}/{self.get_max_pages()}')
        for v in entry.items:
            embed.add_field(name=v[0], value=(
                v[1][:250] + '...') if len(v[1]) > 250 else v[1], inline=False)
        return embed


class NewMenuPages(menus.MenuPages):
    async def update(self, payload):
        if self._can_remove_reactions:
            if payload.event_type == 'REACTION_ADD':
                await self.message.remove_reaction(payload.emoji, payload.member)
            elif payload.event_type == 'REACTION_REMOVE':
                return
        await super().update(payload)


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
