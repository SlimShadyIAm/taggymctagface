import discord
from discord import Embed, Color
from discord.ext import commands, tasks
import feedparser

class CrosBlog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "http://googlechromereleases.blogspot.com/atom.xml"
        self.prev_data = feedparser.parse(self.url)

        self.watcher.start()

    def cog_unload(self):
        self.watcher.cancel()
        print("STOPPING...")

    # the watcher thread
    @tasks.loop(seconds=10)
    async def watcher(self):

def setup(bot):
    bot.add_cog(CrosBlog(bot))