from discord.ext import commands
import feedparser
import pprint
import threading, time

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
                'requiredFilters': ["chromebook", "chromebooks", "chromeos"],
                'good_feed': True,
                'prev_data': feedparser.parse('https://www.androidpolice.com/feed/')

            },
            {
                'feed': "https://www.androidauthority.com/feed/",
                'name': "AndroidAuthority.com",
                'profilePicture':
                    "https://images-na.ssl-images-amazon.com/images/I/51L8Vd5bndL._SY355_.png",
                'filters': ["deal", "deals", "sale", "sales"],
                'requiredFilters': ["chromebook", "chromebooks", "chromeos"],
                'good_feed': True,
                'prev_data': feedparser.parse('https://www.androidauthority.com/feed/')
            }
        ];

        self.stop_event = threading.Event()
        for feed in feeds:
            thread = threading.Thread(target=watcher, args=(feed, self.stop_event,), daemon=True)
            thread.start()

        # self.data = feedparser.parse('https://www.aboutchromebooks.com/feed/')
    def cog_unload(self):
        self.stop_event.set()
        print("STOPPING...")

def watcher(feed, stop_event):   
    pp = pprint.PrettyPrinter(indent=4)

    while not stop_event.is_set():   
        if feed['good_feed'] is True:
            good_feed(feed)
        else:
            bad_feed(feed)
        time.sleep(60)

def good_feed(feed):
    data = feedparser.parse(feed["feed"])
    data = feedparser.parse(feed["feed"], modified=feed["prev_data"].modified)
    if (data.status != 304):
        for post in data.entries:
            print(f'NEW GOOD ENTRY: {post.title} {post.link}')
        check_new_entries(feed, data.entries)
    feed["prev_data"] = data

def bad_feed(feed):
    data = feedparser.parse(feed["feed"])
    prev_ids = [something["id"] for something in feed["prev_data"].entries]
    new_ids = [something["id"] for something in data.entries if something["id"] not in prev_ids]
    
    new_posts = [post for post in data.entries if post.id in new_ids]
    if (len(new_posts) > 0):
        for post in new_posts:
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


def setup(bot):
    dw = DealWatcher(bot)
    bot.add_cog(dw)
