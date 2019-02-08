import discord
import asyncio
import datetime
from discord.ext import commands

LP_CHANNEL_IDS = [419732859360641024, 457320312124604416]
TEST_CHANNEL_IDS = [541472338013847553, 533773210345275401]

CD_ALLOWED = {x: True for x in LP_CHANNEL_IDS}


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
            await ctx.send('Countdown is allowed only in LP channels!')

    @commands.command()
    async def timestamp(self, ctx):
        if ctx.channel.id in CD_ALLOWED:
            spotify = None
            if ctx.author.activities and ctx.author.activities[0] == discord.Spotify:
                spotify = ctx.author.activities[0]
            while spotify == None:
                async for message in ctx.channel.history(limit=50):
                    act = message.author.activities
                    if act and type(act[0]) == discord.Spotify:
                        spotify = act[0]
                    else:
                        continue

            seconds = (datetime.datetime.utcnow() - spotify.start + datetime.timedelta(seconds=3)).total_seconds()
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            if seconds < 10:
                seconds = str(0) + str(int(seconds))
            else:
                seconds = str(int(seconds))

            song = discord.Embed(type='rich', title="Listening Party:", color=2351402)
            song.set_thumbnail(url=spotify.album_cover_url)
            song.add_field(value="[{} - {}](https://open.spotify.com/track/{})".format(spotify.title, spotify.artist, spotify.track_id),
                           name="Currently at {}:{}".format(int(minutes), seconds))

            await ctx.send(embed=song)
        else:
            await ctx.send("Timestamp command is only allowed in LP channels!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def close(self, ctx):
        if 'Mod' in [x.name for x in ctx.author.roles] or 'Dev' in [x.name for x in ctx.author.roles]:
            await ctx.bot.close()


def setup(bot):
    bot.add_cog(Commands(bot))
