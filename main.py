import discord
import os
from discord.ext import commands
import sqlite3

async def on_message(self, message):
    print('Message from {0.author}: {0.content}'.format(message))

initial_extensions = ['cogs.crosupdates', 
                        'cogs.admin', 
                        'cogs.crosblog', 
                        'cogs.dealwatcher', 
                        'cogs.errhandle', 
                        'cogs.add',
                        'cogs.delete', 
                        'cogs.list', 
                        'cogs.board2device', 
                        'cogs.device2board', 
                        'cogs.birthday',
                        'cogs.helpers',
                        'cogs.rolecount'
                    ]

bot = commands.Bot(command_prefix="$", description='A Rewrite Cog Example')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name='Cogs Example', type=1, url='https://twitch.tv/kraken'))
    print(f'Successfully logged in and booted...!')
    conn = sqlite3.connect('commands.sqlite')
    c = conn.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='commands';")
    res = c.fetchone()
    if (res[0] == 0):
        c.execute("CREATE TABLE IF NOT EXISTS commands (command_id INTEGER PRIMARY KEY, server_id TEXT, user_who_added TEXT, command_name TEXT, no_of_uses INTEGER, response TEXT, args TEXT);")
        c.execute("CREATE UNIQUE INDEX idx_command_id ON commands (command_id);")
        print("created!")
    conn.commit()
    conn.close()

bot.run(os.environ.get('TAGGY_TOKEN'), bot=True, reconnect=True)
