import discord
import asyncio
import random
import sys
from discord.ext import commands

token = open('token.txt', 'r').read().strip()

EXTENSIONS = [
    'cogs.commands'
]

LIVE_PREFIX = '$'
TEST_PREFIX = '?'


class ProgBot(commands.Bot):

    def __init__(self):
        # CHANGE TEST TO LIVE FOR DEPLOYED BUILD
        super().__init__(command_prefix=LIVE_PREFIX, description="Images & Words Bot")
        self.token = token

        for ext in EXTENSIONS:
            try:
                self.load_extension(ext)
            except Exception as e:
                print('Failed to load extension {}'.format(ext))

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def close(self):
        await super().close()

    def run(self):
        super().run(self.token, reconnect=True)


if __name__ == '__main__':
    prog_bot = ProgBot()
    prog_bot.run()
