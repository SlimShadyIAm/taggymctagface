import pprint
import threading
import time
import asyncio
import feedparser
from discord.ext import commands, tasks

bott = None

class DealWatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feeds = [
            {
                'feed': "https://www.aboutchromebooks.com/feed/",
                'name': "AboutChromebooks.com",
                'profilePicture':
                    "https://cdn.discordapp.com/emojis/363434654000349184.png?v=1",
                'filters': ["deal", "deals"],
                'requiredFilters': [],
                'good_feed': False,
                'prev_data': feedparser.parse('https://www.aboutchromebooks.com/feed/')
            },
            {
                'feed': "https://www.androidpolice.com/feed/",
                'name': "AndroidPolice.com",
                'profilePicture':
                    "https://lh4.googleusercontent.com/-2lq9WcxRgB0/AAAAAAAAAAI/AAAAAAAAAQk/u15SBRi49fE/s250-c-k/photo.jpg",
                'filters': ["deal", "deals", "sale", "sales"],
                'requiredFilters': ["chromebook", "chromebooks", "chromeos", "chrome os"],
                'good_feed': True,
                'prev_data': feedparser.parse('https://www.androidpolice.com/feed/')

            },
            {
                'feed': "https://www.androidauthority.com/feed/",
                'name': "AndroidAuthority.com",
                'profilePicture':
                    "https://images-na.ssl-images-amazon.com/images/I/51L8Vd5bndL._SY355_.png",
                'filters': ["deal", "deals", "sale", "sales"],
                'requiredFilters': ["chromebook", "chromebooks", "chromeos", "chrome os" "google chrome os"],
                'good_feed': True,
                'prev_data': feedparser.parse('https://www.androidauthority.com/feed/')
            }
        ]

        self.loops = [asyncio.get_event_loop().create_task(self.watcher(feed)) for feed in self.feeds]

    def cog_unload(self):
        [loop.cancel() for loop in self.loops]
        print("STOPPING...")

    # the watcher thread
    async def watcher(self, feed):
        await self.bot.wait_until_ready()
    
        while True:
            if feed['good_feed'] is True:
                await self.good_feed(feed)
            else:
                await self.bad_feed(feed) 
            await asyncio.sleep(10)
        

    # feed watcher for feeds with proper etag support
    
    async def good_feed(self, feed):
        kwargs = dict(modified=feed["prev_data"].modified if hasattr(feed["prev_data"], 'modified') else None, etag=feed["prev_data"].etag if hasattr(feed["prev_data"], 'modified')  else None)
        data = feedparser.parse(feed["feed"], **{k: v for k, v in kwargs.items() if v is not None})

        if (data.status != 304):
            await self.check_new_entries(feed, data.entries)
        
        feed["prev_data"] = data

    # improper etag support
    async def bad_feed(self, feed):
        data = feedparser.parse(feed["feed"])
        max_prev_date = max([something["published_parsed"] for something in feed["prev_data"].entries])
        new_posts = [post for post in data.entries if post["published_parsed"] > max_prev_date]
        if (len(new_posts) > 0):
            for post in new_posts:
                print(f'NEW BAD ENTRY: {post.title} {post.link}')
            await self.check_new_entries(feed, new_posts)   
        feed["prev_data"] = data

    async def check_new_entries(self, feed, entries):
        for entry in entries:
            post_tags = [tag.term.lower() for tag in entry.tags]
            if len(feed["requiredFilters"]) != 0:
                match = [tag for tag in feed["filters"] if tag in post_tags]
                match_required = [tag for tag in feed["requiredFilters"] if tag in post_tags]
                if (len(match) > 0 and len(match_required) > 0):
                    print(f'MATCH FOUND DEAL {entry.title}, {entry.link}, {entry.tags}')
                    await self.push_update(entry, feed)
            else:
                match = [tag for tag in feed["filters"] if tag in post_tags]
                if (len(match) > 0):
                    print(f'MATCH FOUND DEAL {entry.title}, {entry.link}, {entry.tags}')
                    await self.push_update(entry, feed)


    async def push_update(self, post, feed):
        channel = self.bot.get_guild(525250440212774912).get_channel(621704381053534257)
        await (channel.send(f'New deal was posted!\n{post.title}\n{post.link}'))
    
def setup(bot):
    dw = DealWatcher(bot)
    bot.add_cog(dw)
