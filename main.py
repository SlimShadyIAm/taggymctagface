import discord
import os
from discord.ext import commands
import sqlite3


async def on_message(self, message):
    print('Message from {0.author}: {0.content}'.format(message))

initial_extensions = [
    'cogs.add',
    'cogs.admin',
    'cogs.birthday',
    'cogs.board2device',
    'cogs.crosblog',
    'cogs.crosupdates',
    'cogs.dealwatcher',
    'cogs.delete',
    'cogs.device2board',
    'cogs.errhandle',
    'cogs.getkarma',
    'cogs.help',
    'cogs.helpers',
    'cogs.history',
    'cogs.karma',
    'cogs.leaderboard',
    'cogs.list',
    'cogs.modhistory',
    'cogs.ping',
    'cogs.rolecount',
    'cogs.rules',
    'cogs.search',
    'cogs.setkarma',
    'cogs.stats',
    'cogs.timeout'
]

bot = commands.Bot(command_prefix="$",
                   description='Taggy McTagface', case_insensitive=True)

if __name__ == '__main__':
    bot.remove_command("help")
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


@bot.event
async def on_ready():
    print(
        f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(details='over r/ChromeOS', state='over r/ChromeOS', name='over r/ChromeOS', type=discord.ActivityType.watching))
    print(f'Successfully logged in and booted...!')

    try:
        conn = sqlite3.connect('commands.sqlite')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS commands (command_id INTEGER PRIMARY KEY, server_id TEXT, user_who_added TEXT, command_name TEXT, no_of_uses INTEGER, response TEXT, args TEXT);")
        c.execute(
            "CREATE TABLE IF NOT EXISTS karma (user_id INTEGER, guild_id INTEGER, karma INTEGER, notified_good BOOLEAN DEFAULT 0, notified_bad BOOLEAN DEFAULT 0, PRIMARY KEY (user_id, guild_id), CONSTRAINT uid FOREIGN KEY (user_id) REFERENCES users(user_id));")
        c.execute("CREATE TABLE IF NOT EXISTS karma_history (hist_id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, user_id INTEGER, invoker_id INTEGER, amount INTEGER, timestamp DATETIME);")
        c.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, nickname TEXT, UNIQUE(user_id));")
        #c.execute("ALTER TABLE karma_history ADD reason TEXT DEFAULT 'No reason.'")
        conn.commit()
    finally:
        conn.close()


@bot.event
async def on_user_update(_, after):
    await update_users_db(after)


@bot.event
async def on_member_join(member):
    await update_users_db(member)


@bot.event
async def on_member_remove(member):
    await update_users_db(member)


async def update_users_db(member):
    try:
        conn = sqlite3.connect('commands.sqlite')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO users (user_id, nickname) VALUES(?,?)",
                  (member.id, f'{member.name}#{member.discriminator}',))
        conn.commit()
    finally:
        conn.close()

bot.run(os.environ.get('TAGGY_TOKEN'), bot=True, reconnect=True)
