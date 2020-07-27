import asyncio
import os

import discord
import feedparser
from discord import Color, Embed
from discord.ext import commands


class Brunch(commands.Cog):
    """Watch Google's release feed to watch for new ChromeOS updates. Send to Discord channel if found."""

    def __init__(self, bot):
        self.bot = bot
        self.url = "https://github.com/sebanc/brunch/releases.atom"
        self.prev_data = feedparser.parse(self.url)
        # create thread for loop which watches feed
        self.loop = asyncio.get_event_loop().create_task(self.watcher())

    # cancel loop when unloading cog
    def cog_unload(self):
        self.loop.cancel()

    # the watcher thread
    async def watcher(self):
        # wait for bot to start
        await self.bot.wait_until_ready()
        await self.push_update(self.prev_data.entries[0])
        while not self.loop.cancelled():
            kwargs = dict(modified=self.prev_data.modified if hasattr(self.prev_data, 'modified')
                          else None, etag=self.prev_data.etag if hasattr(self.prev_data, 'modified') else None)
            # fetch feed data w/ args
            data = feedparser.parse(
                self.url, **{k: v for k, v in kwargs.items() if v is not None})

            if (data.status != 304):
                # get newest post date from cached data. any new post will have a date newer than this
                max_prev_date = max([something["published_parsed"]
                                     for something in self.prev_data.entries])
                # get new posts
                new_posts = [
                    post for post in data.entries if post["published_parsed"] > max_prev_date]
                # if there rae new posts
                if (len(new_posts) > 0):
                    # check thier tags
                    for post in new_posts:
                        print(f'New Brunch release: {post.title} {post.link}')
                        await self.push_update(post)

            # update local cache
            self.prev_data = data
            # wait 1 minute before checking feed again
            await asyncio.sleep(60)

    async def push_update(self, post):
        # which guild to post to depending on if we're prod or dev
        # post update to channel
        guild_id = 525250440212774912 if os.environ.get(
            'PRODUCTION') == "false" else 253908290105376768
        guild_channels = self.bot.get_guild(guild_id).channels
        guild_roles = self.bot.get_guild(guild_id).roles
        channel = discord.utils.get(guild_channels, name="deals-and-updates")
        role = discord.utils.get(guild_roles, name="Brunch")
        await (channel.send(f'{role.mention} New Brunch release!\n{post.title}\n{post.link}'))


def setup(bot):
    bot.add_cog(Brunch(bot))
