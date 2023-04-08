import discord
import os

client = discord.Client()

client.run(os.getenv('TOKEN'))
