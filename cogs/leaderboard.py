import os
import random
import sqlite3
from os.path import abspath, dirname
from datetime import datetime
import discord
from discord import Color, Embed, Member
from discord.ext import commands, menus

ctx = None


class NewMenuPages(menus.MenuPages):
    async def update(self, payload):
        if self._can_remove_reactions:
            if payload.event_type == 'REACTION_ADD':
                await self.bot.http.remove_reaction(
                    payload.channel_id, payload.message_id,
                    discord.Message._emoji_reaction(
                        payload.emoji), payload.member.id
                )
            elif payload.event_type == 'REACTION_REMOVE':
                return
        await super().update(payload)


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='leaderboard', aliases=["lb"])
    async def leaderboard(self, ctx):
        """(alias $lb) Karma leaderboard in current guild"""

        class Source(menus.GroupByPageSource):
            async def format_page(self, menu, entry):
                embed = Embed(
                    title=f'Leaderboard: Page {menu.current_page +1}/{self.get_max_pages()}', color=Color(value=0xfcba03))
                embed.set_footer(icon_url=ctx.author.avatar_url,
                                 text="Note: Nerds and Moderators were exlcluded from these results.")
                embed.description = ""
                for v in entry.items:
                    member = discord.utils.get(ctx.guild.members, id=v[0])
                    if not member:
                        embed.description += f'**Rank {v[2]}**: {fetch_nick(v[0])} with {v[1]} karma\n'
                    else:
                        if not ctx.channel.permissions_for(member).manage_messages:
                            embed.description += f'**Rank {v[2]}**: {member.mention } with {v[1]} karma\n'
                return embed

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                "SELECT user_id, karma, rank FROM ( SELECT karma, user_id, RANK() OVER ( ORDER BY karma DESC ) rank FROM karma WHERE guild_id = ?);", (ctx.guild.id,))
            data = c.fetchall()

        finally:
            conn.close()

        if (len(data) == 0):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="No history in this guild!"))
        else:
            pages = NewMenuPages(source=Source(
                data, key=lambda t: 1, per_page=10), clear_reactions_after=True)
            await pages.start(ctx)

    @ leaderboard.error
    async def leaderboard_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}\nExample usage: `$history` or $history @member'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))
        else:
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))


def fetch_nick(id):
    BASE_DIR = dirname(dirname(abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "commands.sqlite")
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            "SELECT nickname FROM users WHERE user_id = ?", (id,))
        data = c.fetchall()

    finally:
        conn.close()
    return data[0][0]


def setup(bot):
    bot.add_cog(CustomCommands(bot))
