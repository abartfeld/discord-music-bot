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

    # async def on_reaction(self, react):

    async def close(self):
        await super().close()

    def run(self):
        super().run(self.token, reconnect=True)

if __name__ == '__main__':
    prog_bot = ProgBot()
    prog_bot.run()
