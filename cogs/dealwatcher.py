from discord.ext import commands, tasks
import feedparser
import pprint
import threading, time
import asyncio
from syncer import sync

bott = None

class DealWatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        feeds = [
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

        for feed in feeds:
            thread = threading.Thread(target=watcher, args=(feed, bot,), daemon=True)
            thread.start()

        # loop.run_forever()
    def cog_unload(self):
        # loop = asyncio.get_event_loop()
        # loop.close()
        print("STOPPING...")

# the watcher thread
@tasks
def watcher(feed, bot):
    print("Starting watcher...")   
    pp = pprint.PrettyPrinter(indent=4)

    while True:
        if feed['good_feed'] is True:
            good_feed(feed, bot)
        else:
            bad_feed(feed, bot)
        time.sleep(60)

# feed watcher for feeds with proper etag support
def good_feed(feed, bot):
    data = feedparser.parse(feed["feed"])
    data = feedparser.parse(feed["feed"], modified=feed["prev_data"].modified)
    if (data.status != 304):
        for post in data.entries:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(push_update(post, feed, bot))
            print(f'NEW GOOD ENTRY: {post.title} {post.link}')
        check_new_entries(feed, data.entries)
    feed["prev_data"] = data

# improper etag support
def bad_feed(feed, bot):
    data = feedparser.parse(feed["feed"])
    for post in data.entries:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(push_update(post, feed, bot))
    prev_ids = [something["id"] for something in feed["prev_data"].entries]
    new_ids = [something["id"] for something in data.entries if something["id"] not in prev_ids]
    
    new_posts = [post for post in data.entries if post.id in new_ids]
    if (len(new_posts) > 0):
        for post in new_posts:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(push_update(post, feed, bot))
            print(f'NEW BAD ENTRY: {post.title} {post.link}')
        check_new_entries(feed, new_posts)


def check_new_entries(feed, entries):
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(entries)
    for entry in entries:
        post_tags = [tag.term.lower() for tag in entry.tags]
        if len(feed["requiredFilters"]) != 0:
            match = [tag for tag in feed["filters"] if tag in post_tags]
            match_required = [tag for tag in feed["requiredFilters"] if tag in post_tags]
            if (len(match) > 0 and len(match_required) > 0):
                print(f'MATCH FOUND {entry.title}, {entry.link}, {entry.tags}')
        else:
            match = [tag for tag in feed["filters"] if tag in post_tags]
            if (len(match) > 0):
                print(f'MATCH FOUND {entry.title}, {entry.link}, {entry.tags}')

async def push_update(post, feed, bot):
    channel = bot.get_guild(525250440212774912).get_channel(621704381053534257)
    await (channel.send(f'NEW ENTRY: {post.title} {post.link} {feed["name"]}'))
def setup(bot):
    dw = DealWatcher(bot)
    bot.add_cog(dw)

