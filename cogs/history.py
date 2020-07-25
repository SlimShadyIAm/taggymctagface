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

    @commands.command(name='history')
    async def history(self, ctx, member: Member = None):
        """History of all karma, or a specific user's karma\nExample usage: `$history` or `$history @member`"""

        class Source(menus.GroupByPageSource):
            async def format_page(self, menu, entry):
                embed = Embed(
                    title=f'History: Page {menu.current_page +1}/{self.get_max_pages()}', color=Color(value=0xfcba03))
                for v in entry.items:
                    member = discord.utils.get(ctx.guild.members, id=v[2])
                    member_text = ""
                    if not member:
                        member_text = fetch_nick(v[2])
                    invoker_text = ""
                    invoker = discord.utils.get(ctx.guild.members, id=v[3])
                    if not invoker:
                        invoker_text = fetch_nick(v[3])

                    embed.add_field(
                        name=f'{v[0]}. {datetime.strptime(v[5], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")}', value=f'{invoker.mention if invoker else invoker_text} {f"gave {v[4]} karma to" if v[4] > 0 else f"took {-1 * v[4]} karma from "} {member.mention if member else member_text}\nReason:{v[6]}', inline=False)
                return embed

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        if member is None:
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "SELECT * FROM karma_history WHERE guild_id = ? ORDER BY timestamp DESC", (ctx.guild.id,))
                data = c.fetchall()

            finally:
                conn.close()

            if (len(data) == 0):
                await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="No history for this user!"))

            else:
                pages = NewMenuPages(source=Source(
                    data, key=lambda t: 1, per_page=10), clear_reactions_after=True)
                await pages.start(ctx)
        else:
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute(
                    "SELECT * FROM karma_history WHERE guild_id = ? AND user_id = ? ORDER BY timestamp DESC", (ctx.guild.id, member.id,))
                data = c.fetchall()

            finally:
                conn.close()

            if (len(data) == 0):
                await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="No history in this guild!"))
            else:
                pages = NewMenuPages(source=Source(
                    data, key=lambda t: 1, per_page=10), clear_reactions_after=True)
                await pages.start(ctx)

    @history.error
    async def history_err(self, ctx, error):
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
