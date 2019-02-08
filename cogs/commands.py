import discord
import asyncio
import datetime
from discord.ext import commands

LP_CHANNEL_IDS = [419732859360641024, 457320312124604416]
TEST_CHANNEL_IDS = [541472338013847553, 533773210345275401]


class Commands:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cd(self, ctx):
        """Auto countdown from 10 for LPs. Only allowed in LP channels."""
        if ctx.channel.id in LP_CHANNEL_IDS:
            await ctx.send('Counting down!')
            await asyncio.sleep(2)
            for i in range(10, 0, -1):
                await ctx.send(i)
                await asyncio.sleep(1)
            await ctx.send('GO')
        else:
            await ctx.send('Countdown is allowed only in LP channels!')

    @commands.command()
    async def timestamp(self, ctx):
        if ctx.channel.id in LP_CHANNEL_IDS:
            spotify = None
            if ctx.author.activities:
                spotify = find_spotify(ctx.author.activities)
            # if author is not playing spotify
            if spotify == None:
                async for message in ctx.channel.history(limit=50):
                    spotify = find_spotify(message.author.activities)
                    if spotify:
                        break
            # if nobody in past 50 messages is playing spotify
            if spotify == None:
                await ctx.send("Can't find timestamp info!")
                return

            seconds = (datetime.datetime.utcnow() - spotify.start + datetime.timedelta(seconds=3)).total_seconds()
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            seconds = str(int(seconds)).zfill(2)

            song = discord.Embed(type='rich', title="Listening Party", color=2351402)
            song.set_thumbnail(url=spotify.album_cover_url)
            song.add_field(value="[{} - {}](https://open.spotify.com/track/{})".format(spotify.artist, spotify.title,
                                                                                       spotify.track_id),
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


def find_spotify(act):
    for a in act:
        if isinstance(a, discord.Spotify):
            return a
    return None


def setup(bot):
    bot.add_cog(Commands(bot))
