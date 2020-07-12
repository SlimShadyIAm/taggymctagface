from discord import Embed, Color
from discord.ext import commands
import sqlite3
import random
from os.path import dirname, abspath
import os
class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='delete', description="blah")
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, id):
        """Delete a custom command\nExample usage: `$delete 12345`"""
        
        if not id.isnumeric():
            raise commands.BadArgument("You need to supply a numeric command ID to delete!\nExample usage: `$delete 12345`")

        BASE_DIR = dirname(dirname(abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "commands.sqlite")
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(f"SELECT * FROM commands WHERE server_id = {ctx.guild.id} AND command_id = ?;", (id,))

            if len(c.fetchall()) == 0:
                await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="There is no command with that ID!"))
                return

            c.execute(f"DELETE FROM commands WHERE server_id = {ctx.guild.id} AND command_id = ?", (id,))
            conn.commit()
        finally:
            conn.close()
        
        await ctx.send(embed=Embed(title=f"Deleted command!", color=Color(value=0x37b83b), description=f'Command with ID {id} is deleted'))

    @delete.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description=f'{error}'))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=Embed(title="An error occured!", color=Color(value=0xEB4634), description="You don't have permission to do this command!"))


def setup(bot):
    bot.add_cog(CustomCommands(bot))

