import discord
import os
from discord.ext import commands

async def on_message(self, message):
    print('Message from {0.author}: {0.content}'.format(message))

initial_extensions = ['cogs.crosupdates', 'cogs.admin', 'cogs.crosblog', 'cogs.dealwatcher']

bot = commands.Bot(command_prefix="$", description='A Rewrite Cog Example')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name='Cogs Example', type=1, url='https://twitch.tv/kraken'))
    print(f'Successfully logged in and booted...!')

bot.run(os.environ.get('TAGGY_TOKEN'), bot=True, reconnect=True)
