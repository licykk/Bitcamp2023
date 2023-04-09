import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import logging
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')


intents = discord.Intents.default()
intents.message_content = True

# We are using the commands framework from discord.py
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as ' + str(bot.user))

@bot.command()
async def hello(ctx):
    await ctx.send('Hello! :plead:')

# if __name__ == "__main__":
#     # When running this file, if it is the 'main' file
#     # I.E its not being imported from another python file run this
#     for file in os.listdir("cogs"):
#         if file.endswith(".py") and not file.startswith("_"):
#             print(file)
#             bot.load_extension(f"cogs.{file[:-3]}")

#     bot.run(TOKEN)

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())