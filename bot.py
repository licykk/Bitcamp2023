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
from colorama import Back, Fore, Style
import datetime

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

@bot.tree.command(description="Create customer")
async def create(interaction: discord.Interaction, first_name: str, last_name: str):
    customer_id = create_customer(first_name, last_name, "123", "Filler", "Filler", "MD", "20871")
    await interaction.response.send_message("Customer created for " + first_name + " " + last_name)
    run_transaction(sessionmaker(bind=ENGINE), 
                    lambda s: create_customer_db(s, interaction.user.id, customer_id))

@bot.tree.command(description="Create account")
async def setupaccount(interaction: discord.Interaction):
    cust_id = run_transaction(sessionmaker(bind=ENGINE),
                              lambda s: get_customer_db(s, interaction.user.id))
    cust_id = cust_id.strip()
    print("Customer ID:", cust_id)
        
    act_type = "Checking"
    nickname = f"Account for {interaction.user}"
    rewards = 1000
    balance = 1000
    act_num = "1234567890123456"

    account_cnt = count_cust_accounts(cust_id)

    if account_cnt >= 1:
        await interaction.response.send_message("You already have an account")
        return
    elif account_cnt == -1:
        await interaction.response.send_message("Request error checking account count")
        return
    
    acct_id = create_account(cust_id, act_type, nickname, rewards, balance, act_num)
    print(acct_id)
    run_transaction(sessionmaker(bind=ENGINE),
                    lambda s: create_account_db(s, cust_id, acct_id))
    
    await interaction.response.send_message("Created account for customer " + interaction.user.mention)




@bot.tree.command(description="Gets information on a user. Defaults to the user who ran the command.")
async def userinfo(interaction: discord.Interaction):
    embed = discord.Embed(title="User Info", description=f"Here's the user information for {interaction.user}", color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=interaction.user.avatar)
    embed.add_field(name="User ID", value=interaction.user.id)
    embed.add_field(name="User Name", value=f'{interaction.user.name}#{interaction.user.discriminator}')
    embed.add_field(name="Nickname", value=interaction.user.display_name)

    print('before database')
    cust_id = run_transaction(sessionmaker(bind=ENGINE),
                lambda s: get_customer_db(s, interaction.user.id))
    cust_id = cust_id.strip()

    cust_accts = get_cust_accounts(cust_id)

    print(cust_accts)
    for k, v in cust_accts.items():
        print(v)
        embed.add_field(name="Account balance", value=v)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(description="Requests a user to pay a certain amount of money to you.")
async def requestpayment(interaction: discord.Interaction, member: discord.Member, amount: int, comment: str=None):
    #embed: discord.Embed = discord.Embed(title="Payment Request", description=f"{interaction.user.mention} has requested ${amount} from {member.mention}", color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
    if comment is None:
        await interaction.response.send_message(content=f'{interaction.user.mention} has requested ${amount} from {member.mention}.')
    await interaction.response.send_message(content=f'{interaction.user.mention} has requested ${amount} from {member.mention}. \n Comments: {comment}')


@bot.tree.command(description="Pays a user a certain amount of money.")
async def pay(interaction: discord.Interaction, member: discord.Member, amount: int, comment: str=None):
     

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
    if comment is None:
        transaction_id = create_transaction(sender_acct, medium, receiver_acct, "N/A", amount)
    else:
        transaction_id = create_transaction(sender_acct, medium, receiver_acct, comment, amount)

    if transaction_id is None:
        await interaction.response.send_message("Transaction failed (insufficient funds?)")
    else:
        if comment is None:
            await interaction.response.send_message(content=f'{interaction.user.mention} has paid ${amount} to {member.mention}.')
        else:
            await interaction.response.send_message(content=f'{interaction.user.mention} has paid ${amount} to {member.mention}. \n Comments: {comment}')


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