import discord
from discord.ext import commands
import random

class Splitwise(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='split', help='split bill')
    async def split_bill(self, ctx, cost, *splitters: discord.Member):
             
        if ctx.author.bot:
            return
        
        try:
            cost = round(float(cost),2)
        except: 
            await ctx.send(f"Invalid cost value: {cost}. Please input a valid number.")  
            return
        
        split_cost = round(cost / len(splitters),2)
        remaining_cost = round(cost - len(splitters) * split_cost,2) # Note: can be negative
        special_user = random.choice(range(len(splitters)))
        
        # Determine who is the special user to pay a different amount if the bill can't be split equally
        splitters_embed_text = ""
        cost_embed_text = ""
        for i, user in enumerate(splitters):
            splitters_embed_text += f"{user}\n"
            if i == special_user:
                cost_embed_text += f"${split_cost+remaining_cost:.2f}\n"
            else:
                cost_embed_text += f"${split_cost:.2f}\n"
        
        embed = discord.Embed(
            title="Split the Bill!",
            color=0x808080,
            timestamp=ctx.message.created_at
        )

        # Double embed field used to get costs to align properly in the card
        embed.add_field(
            name=splitters_embed_text,
            value='\uFEFF',
            inline=True
        )

        embed.add_field(
            name=cost_embed_text,
            value='\uFEFF',
            inline=True
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Splitwise(bot))