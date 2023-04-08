import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)
'''
@client.event
async def on_ready():
    print('We have logged in as ' + str(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
'''
@bot.command()
async def payTo(ctx, member: discord.Member, amt: int): # command, arguments
    cmd_issuer = ctx.author
    msg = str(cmd_issuer) + ' paying ' + str(amt) + ' to ' + str(member)
    await ctx.send(msg)

bot.run(os.getenv('TOKEN'))
