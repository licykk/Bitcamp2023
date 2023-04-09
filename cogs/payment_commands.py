import discord
from discord.ext import commands
from discord import app_commands
import datetime

from payments import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from database_functions import *

DB_URI = os.environ['DATABASE_URL'].replace("postgresql://", "cockroachdb://")
try:
    print("Trying to connect to database...")
    ENGINE = create_engine(DB_URI, connect_args={"application_name":"docs_simplecrud_sqlalchemy"})
    print("Done")
except Exception as e:
    print("Failed to connect to database.")
    print(f"{e}")

class PaymentCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @app_commands.command(description="Gets information on a user. Defaults to the user who ran the command.")
    async def returnaccount(self, interaction: discord.Interaction, member: discord.Member=None):
        if member is None:
            member = interaction.user
        embed = discord.Embed(title="User Info", description=f"Here's the user information for {member}", color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="User ID", value=member.id)
        embed.add_field(name="User Name", value=f'{member.name}#{member.discriminator}')
        embed.add_field(name="Nickname", value=member.display_name)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Requests a user to pay a certain amount of money to you.")
    async def requestpayment(self, interaction: discord.Interaction, member: discord.Member, amount: int, comment: str=None):
        if comment is None:
            await interaction.response.send_message(content=f'{interaction.user.mention} has requested ${amount} from {member.mention}.')
        await interaction.response.send_message(content=f'{interaction.user.mention} has requested ${amount} from {member.mention}. \n Comments: {comment}')

    @app_commands.command(description="Pays a user a certain amount of money to you.")
    async def pay(self, interaction: discord.Interaction, member: discord.Member, amount: int, comment: str=None):
        if comment is None:
            await interaction.response.send_message(content=f'{interaction.user.mention} has paid ${amount} to {member.mention}.')
        await interaction.response.send_message(content=f'{interaction.user.mention} has paid ${amount} to {member.mention}. \n Comments: {comment}')
    
        
async def setup(bot):
    await bot.add_cog(PaymentCommands(bot))