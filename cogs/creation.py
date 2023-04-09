from discord.ext import commands
from payments import *

class Creation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx, first_name: str, last_name: str, *args):
        create_customer(first_name, last_name, args[0], args[1], args[2], args[3], args[4])


async def setup(bot):
    await bot.add_cog(Creation(bot))