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
    'cogs.help',
    'cogs.helpers',
    'cogs.history',
    'cogs.karma',
    'cogs.list',
    'cogs.ping',
    'cogs.rolecount',
    'cogs.rules',
    'cogs.search',
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
            "CREATE TABLE IF NOT EXISTS karma (user_id INTEGER, guild_id INTEGER, karma INTEGER, PRIMARY KEY (user_id, guild_id));")
        c.execute("CREATE TABLE IF NOT EXISTS karma_history (hist_id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, user_id INTEGER, invoker_id INTEGER, amount INTEGER, timestamp DATETIME);")
        conn.commit()
    finally:
        conn.close()

bot.run(os.environ.get('TAGGY_TOKEN'), bot=True, reconnect=True)
