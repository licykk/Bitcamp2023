import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import logging
import asyncio
from database_functions import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from payments import *

DB_URI = os.environ['DATABASE_URL'].replace("postgresql://", "cockroachdb://")
try:
    print("Trying to connect to database...")
    ENGINE = create_engine(DB_URI, connect_args={"application_name":"docs_simplecrud_sqlalchemy"})
    print("Done")
except Exception as e:
    print("Failed to connect to database.")
    print(f"{e}")

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
    synced = await bot.tree.sync()

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

@bot.tree.command(description="Gets information on a user. Defaults to the user who ran the command.")
async def whois(interaction: discord.Interaction, member: discord.Member=None):
    if member is None:
        member = interaction.user
    embed = discord.Embed(title="User Info", description=f"Here's the user information for {member}", color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="User ID", value=member.id)
    embed.add_field(name="User Name", value=f'{member.name}#{member.discriminator}')
    embed.add_field(name="Nickname", value=member.display_name)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Requests a user to pay a certain amount of money to you.")
async def requestpayment(interaction: discord.Interaction, member: discord.Member, amount: int, comment: str=None):
    #embed: discord.Embed = discord.Embed(title="Payment Request", description=f"{interaction.user.mention} has requested ${amount} from {member.mention}", color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
    if comment is None:
        await interaction.response.send_message(content=f'{interaction.user.mention} has requested ${amount} from {member.mention}.')
    await interaction.response.send_message(content=f'{interaction.user.mention} has requested ${amount} from {member.mention}. \n Comments: {comment}')


@bot.tree.command(description="Pays a user a certain amount of money.")
async def pay(interaction: discord.Interaction, member: discord.Member, amount: int, comment: str=None):
    if comment is None:
        comment = "N/A" 
        await interaction.response.send_message(content=f'{interaction.user.mention} has paid ${amount} to {member.mention}.')
    else:
        await interaction.response.send_message(content=f'{interaction.user.mention} has paid ${amount} to {member.mention}. \n Comments: {comment}')

    sender_customer_id = run_transaction(sessionmaker(bind=ENGINE),
                lambda s: get_customer_db(s, interaction.user.id))
    sender_customer_id = sender_customer_id.strip()

    receiver_customer_id = run_transaction(sessionmaker(bind=ENGINE),
                lambda s: get_customer_db(s, member.id))
    receiver_customer_id = receiver_customer_id.strip()

    sender_acct = run_transaction(sessionmaker(bind=ENGINE),
                lambda s: get_account_db(s, sender_customer_id))
    sender_acct = sender_acct.strip()

    receiver_acct = run_transaction(sessionmaker(bind=ENGINE),
                lambda s: get_account_db(s, receiver_customer_id))
    receiver_acct = receiver_acct.strip()
            
    print(receiver_acct)

    medium = 'balance'
    await create_transaction(sender_acct, medium, receiver_acct, comment, amount)

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