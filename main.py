import discord
from discord.ext import commands
import random
import asyncio
import time

description = "images & words bot!"
bot = commands.Bot(command_prefix='$', description=description)
LP_CHANNEL_IDS = [419732859360641024, 457320312124604416]
TEST_CHANNEL_IDS = [539174471504756757, 419732859360641024, 457320312124604416, 430646748487221261, 455253321067003927]

#CD_ALLOWED = {x: True for x in LP_CHANNEL_IDS}
CD_ALLOWED = {x: True for x in TEST_CHANNEL_IDS}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def cd(ctx):
    """Auto countdown from 10 for LPs. Only allowed in LP channels."""
    if ctx.channel.id in CD_ALLOWED:
        if CD_ALLOWED[ctx.channel.id]:
            CD_ALLOWED[ctx.channel.id] = False
            await ctx.send('Counting down!')
            await asyncio.sleep(2)
            for i in range(10,0, -1):
                await ctx.send(i)
                await asyncio.sleep(1)
            await ctx.send('GO')
            CD_ALLOWED[ctx.channel.id] = True
    else:
        await ctx.send('Countdown is allowed only in LP channels.')



# Make sure you have a token.txt in the same directory as main.py containing ONLY the bot token
token = open('token.txt', 'r').read()
bot.run(token)
