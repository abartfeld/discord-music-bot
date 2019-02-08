import discord
import asyncio
from datetime import datetime
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

    @commands.command()
    async def timestamp(self, ctx):
        spotify = None
        while spotify == None:
            async for message in ctx.channel.history(limit=50):
                try:
                    act = message.author.activities[0]
                except:
                    continue

                if type(act) == discord.Spotify:
                    spotify = act

        seconds = (datetime.utcnow() - spotify.start).total_seconds()
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if seconds < 10:
            seconds = str(0) + str(int(seconds))
        else:
            seconds = str(int(seconds))

        song = discord.Embed(type='rich', title="Now Playing")
        song.set_thumbnail(url=spotify.album_cover_url)
        song.add_field(value="{} - {}".format(spotify.title, spotify.artist),
                       name="Currently at {}:{}".format(int(minutes), seconds))

        await ctx.send(embed=song)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def close(self, ctx):
        if 'Mod' in [x.name for x in ctx.author.roles] or 'Dev' in [x.name for x in ctx.author.roles]:
            await ctx.bot.close()


def setup(bot):
    bot.add_cog(Commands(bot))
