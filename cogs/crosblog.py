import discord
from discord import Embed, Color
from discord.ext import commands
import asyncio
import feedparser

class CrosBlog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "http://feeds.feedburner.com/GoogleChromeReleases"
        self.prev_data = feedparser.parse(self.url)

        self.loop = asyncio.get_event_loop().create_task(self.watcher())

    def cog_unload(self):
        self.loop.cancel()
        print("STOPPING...")

    
    # the watcher thread
    async def watcher(self):
        await self.bot.wait_until_ready()
        while True:
            kwargs = dict(modified=self.prev_data.modified if hasattr(self.prev_data, 'modified') else None, etag=self.prev_data.etag if hasattr(self.prev_data, 'modified')  else None)
            data = feedparser.parse(self.url, **{k: v for k, v in kwargs.items() if v is not None})

            if (data.status == 304):
                await self.check_new_entries(data.entries)
            self.prev_data = data
            await asyncio.sleep(10)
            

    async def check_new_entries(self, posts):
        for post in posts:
            tags = [thing["term"] for thing in post["tags"]]
            if "Chrome OS" in tags:
                if "Stable updates" in tags:
                    await self.push_update(post, "Stable updates")
                elif "Beta updates" in tags:
                    await self.push_update(post, "Beta updates")
                elif "Dev updates" in tags:
                    await self.push_update(post, "Dev updates")
                elif "Canary updates" in tags:
                    await self.push_update(post, "Canary updates")
        pass

    async def push_update(self, post, category=None):
        if (category is None):
            channel = self.bot.get_guild(525250440212774912).get_channel(621704381053534257)
            await (channel.send(f'New blog was posted!\n{post.title}\n{post.link}'))
        else:
            channel = self.bot.get_guild(525250440212774912).get_channel(621704381053534257)
            await (channel.send(f'New blog was posted for {category} channel!\n{post.title}\n{post.link}'))
        
def setup(bot):
    bot.add_cog(CrosBlog(bot))