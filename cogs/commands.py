import discord
import asyncio
import time
from discord.ext import commands

# LP_CHANNEL_IDS = [419732859360641024, 457320312124604416]
TEST_CHANNEL_IDS = [539174471504756757]

CD_ALLOWED = {x: True for x in TEST_CHANNEL_IDS}

class Commands:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cd(self, ctx):
        """Auto countdown from 10 for LPs. Only allowed in LP channels."""
        if ctx.channel.id in CD_ALLOWED:
            if CD_ALLOWED[ctx.channel.id]:
                CD_ALLOWED[ctx.channel.id] = False
                await ctx.send('Counting down!')
                await asyncio.sleep(2)
                for i in range(10, 0, -1):
                    await ctx.send(i)
                    await asyncio.sleep(1)
                await ctx.send('GO')
                CD_ALLOWED[ctx.channel.id] = True
        else:
            await ctx.send('Countdown is allowed only in LP channels.')


def setup(bot):
    bot.add_cog(Commands(bot))