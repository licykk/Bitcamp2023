import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import logging



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

bot.run(TOKEN)