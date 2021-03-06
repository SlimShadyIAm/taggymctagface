import os
import random
import sqlite3
from typing import Union
from datetime import datetime
from os.path import abspath, dirname

import discord
from discord import Color, Embed, Member
from discord.ext import commands, menus


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='getkarma', aliases=["getrank"])
    async def getkarma(self, ctx, member: Union[Member, int]):
        """(alias $getrank) Get a user's karma\nWorks with ID if the user has left the guild\nExample usage: `$getkarma @member` or `$getkarma 2342492304928`"""

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        embed = Embed(
            title=f"Karma results for {member.name}#{member.discriminator}", color=Color(value=0x37b83b))
        embed.set_footer(
            text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        if isinstance(member, Member):
            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("SELECT karma, rank FROM ( SELECT karma, user_id, RANK() OVER ( ORDER BY karma DESC ) rank FROM karma WHERE guild_id = ?) WHERE user_id = ?;", (ctx.guild.id, member.id,))
                data = c.fetchall()
            finally:
                conn.close()

            embed.add_field(
                name="Karma", value=f'{member.mention} has {data[0][0] if len(data) > 0 else "0"} karma')
            if len(data) > 0:
                embed.add_field(
                    name="Rank", value=f'{member.mention} is ranked {data[0][1]} on the leaderboard')
            else:
                embed.add_field(
                    name="Rank", value=f'{member.mention} is not on the leaderboard as no one has given them karma yet', inline=False)
        else:
            member_obj = discord.utils.get(ctx.guild.members, id=member)
            if member_obj is None:
                try:
                    conn = sqlite3.connect(db_path)
                    c = conn.cursor()
                    c.execute(
                        "SELECT nickname FROM users WHERE user_id = ?", (member,))
                    data = c.fetchall()
                finally:
                    conn.close()

                if len(data) == 0:
                    raise commands.BadArgument(
                        "Couldn't find a user with the given ID. Either they have no karma or it's an invalid ID.")
                else:
                    nickname = data[0][0]
                    try:
                        conn = sqlite3.connect(db_path)
                        c = conn.cursor()
                        c.execute(
                            "SELECT karma, rank FROM ( SELECT karma, user_id, RANK() OVER ( ORDER BY karma DESC ) rank FROM karma WHERE guild_id = ?) WHERE user_id = ?;", (ctx.guild.id, member,))
                        data = c.fetchall()
                    finally:
                        conn.close()

                    if len(data) > 0:
                        embed.add_field(
                            name="Rank", value=f'{nickname} is ranked {data[0][1]} on the leaderboard')
                    else:
                        embed.add_field(
                            name="Rank", value=f'{nickname} is not on the leaderboard as no one has given them karma yet', inline=False)
            else:
                try:
                    conn = sqlite3.connect(db_path)
                    c = conn.cursor()
                    c.execute(
                        "SELECT karma, rank FROM ( SELECT karma, user_id, RANK() OVER ( ORDER BY karma DESC ) rank FROM karma WHERE guild_id = ?) WHERE user_id = ?;", (ctx.guild.id, member.id,))
                    data = c.fetchall()
                finally:
                    conn.close()
                if len(data) > 0:
                    embed.description = f'{member.name}#{member.discriminator} has {data[0][2]} karma'
                else:
                    embed.description = f'{member.name}#{member.discriminator} has 0 karma'
        await ctx.send(embed=embed)

    @ getkarma.error
    async def getkarma_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}\nExample usage: `$karma give @member 3` or `$karma take <ID> 3`'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))
        else:
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))


def setup(bot):
    bot.add_cog(CustomCommands(bot))
