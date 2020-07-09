from discord.ext import commands
import feedparser
import pprint
class DealWatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = feedparser.parse('https://www.aboutchromebooks.com/feed/')
    
    def watcher(self):
        new_data = feedparser.parse('https://www.aboutchromebooks.com/feed/')
    
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(entry)
        xd = [something["id"] for something in self.data.entries]
        for entry in new_data.entries:
            pp.pprint(entry)
            if entry.id not in xd:
                print(entry)

        pass

    

def setup(bot):
    dw = DealWatcher(bot)
    bot.add_cog(dw)
    dw.watcher()
