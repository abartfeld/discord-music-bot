import discord
import asyncio
import random
import sys

from discord.ext import commands

token = open('token.txt', 'r').read()

EXTENSIONS = ['cogs.commands']

class ProgBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='$', description="Images & Words Bot")
        self.token = token

        for ext in EXTENSIONS:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f'Failed to load extension {ext}', file=sys.stderr)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    # async def on_reaction(self, react):

    def run(self):
        super().run(self.token, reconnect=True)

if __name__ == '__main__':
    prog_bot = ProgBot()
    prog_bot.run()
