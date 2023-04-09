from discord.ext import commands
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

class Creation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='create', description="Create customer")
    async def create(self, ctx, first_name: str, last_name: str, *args):
        customer_id = create_customer(first_name, last_name, args[0], args[1], args[2], args[3], args[4])
        print(customer_id)
        print(ctx.author)
        run_transaction(sessionmaker(bind=ENGINE),
                    lambda s: create_customer_db(s, ctx.author.id, customer_id))
        
    @commands.command(name='setupAccount', description="Create account")
    async def create_account(self, ctx):

        cust_id = run_transaction(sessionmaker(bind=ENGINE),
                    lambda s: get_customer_db(s, ctx.author.id))
        print("Customer ID:", cust_id)
        return
        act_type = "Checking"
        nickname = f"Account for {ctx.author}"
        rewards = 1000
        balance = 1000
        act_num = "123456789012345"

        acct_id = create_account(cust_id, act_type, nickname, rewards, balance, act_num)
        print(acct_id)
        run_transaction(sessionmaker(bind=ENGINE),
                    lambda s: create_account_db(s, cust_id, acct_id))
        
    
        



async def setup(bot):
    await bot.add_cog(Creation(bot))