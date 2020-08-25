import asyncio
import os

import discord
from discord import Color, Embed
from discord.ext import commands, tasks


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rolecount.start()

    def cog_unload(self):
        self.rolecount.cancel()

    @tasks.loop(seconds=30)
    async def rolecount(self):
        """Track number of users with a given role"""
        guild_id = 525250440212774912 if os.environ.get(
            'PRODUCTION') == "false" else 253908290105376768
        guild = self.bot.get_guild(guild_id)
        guild_channels = guild.channels
        channel = discord.utils.get(guild_channels, name="assign-roles")
        messages = await channel.history(limit=10).flatten()

        roles_to_track = ["iOS", "macOS", "watchOS"] if os.environ.get('PRODUCTION') == "false" else [
            "Acer",
            "HP",
            "Samsung",
            "Google",
            "Asus",
            "Lenovo",
            "Toshiba",
            "Dell",
            "LG",
            "Stable Channel",
            "Beta Channel",
            "Dev Channel",
            "Canary Channel",
            "Developer Mode",
            "Helpers",
            "Announcements",
            "Deals",
            "Chromium",
        ]
        response = "These statistics reload every 30 seconds.\n"
        for role in roles_to_track:
            role_obj = discord.utils.get(guild.roles, name=role)
            if (role_obj is not None):
                response += f'<@&{role_obj.id}> has {len(role_obj.members)} members\n'
        embed = Embed(title="Role statistics", description=response)
        for message in messages:
            if (message.author == self.bot.user):
                await message.edit(embed=embed)
                return

        await channel.send(embed=embed)

    @rolecount.before_loop
    async def before_rolecount(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Utilities(bot))
