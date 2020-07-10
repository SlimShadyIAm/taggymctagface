from discord.ext import commands, tasks
import feedparser
import pprint
import threading, time

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

        self.watcher.start()

    def cog_unload(self):
        self.watcher.cancel()
        print("STOPPING...")

    # the watcher thread
    @tasks.loop(minues=5)
    async def watcher(self):
        pp = pprint.PrettyPrinter(indent=4)
        for feed in self.feeds:
            if feed['good_feed'] is True:
                await self.good_feed(feed)
            else:
                await self.bad_feed(feed)

    # feed watcher for feeds with proper etag support
    async def good_feed(self, feed):
        data = feedparser.parse(feed["feed"], modified=feed["prev_data"].modified)
        if (data.status != 304):
            for post in data.entries:
                print(f'NEW GOOD ENTRY: {post.title} {post.link}')
            self.check_new_entries(feed, data.entries)
        
        feed["prev_data"] = data

    # improper etag support
    async def bad_feed(self, feed):
        data = feedparser.parse(feed["feed"])
        prev_ids = [something["id"] for something in feed["prev_data"].entries]
        new_ids = [something["id"] for something in data.entries if something["id"] not in prev_ids]
        
        new_posts = [post for post in data.entries if post.id in new_ids]
        if (len(new_posts) > 0):
            for post in new_posts:
                print(f'NEW BAD ENTRY: {post.title} {post.link}')
            self.check_new_entries(feed, new_posts)
        
        feed["prev_data"] = data

    async def check_new_entries(self, feed, entries):
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(entries)
        for entry in entries:
            post_tags = [tag.term.lower() for tag in entry.tags]
            if len(feed["requiredFilters"]) != 0:
                match = [tag for tag in feed["filters"] if tag in post_tags]
                match_required = [tag for tag in feed["requiredFilters"] if tag in post_tags]
                if (len(match) > 0 and len(match_required) > 0):
                    print(f'MATCH FOUND {entry.title}, {entry.link}, {entry.tags}')
                    await self.push_update(entry, feed)
            else:
                match = [tag for tag in feed["filters"] if tag in post_tags]
                if (len(match) > 0):
                    print(f'MATCH FOUND {entry.title}, {entry.link}, {entry.tags}')
                    await self.push_update(entry, feed)


    async def push_update(self, post, feed):
        channel = self.bot.get_guild(525250440212774912).get_channel(621704381053534257)
        await (channel.send(f'New deal was posted!\n{post.title}\n{post.link}'))
      
def setup(bot):
    dw = DealWatcher(bot)
    bot.add_cog(dw)

