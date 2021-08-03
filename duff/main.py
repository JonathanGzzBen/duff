#!/usr/bin/env python3
import discord
from dotenv import dotenv_values

config = dotenv_values(".env")

class DuffClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    
    async def on_message(self, message: discord.Message):
        if message.author == client.user:
            return
        print('Message from {0.author}: {0.content}'.format(message))
        await self.answer_callate(message)
    
    async def answer_callate(self, message: discord.Message):
        await message.reply("callate")

client = DuffClient()
client.run(config["DISCORD_TOKEN"])
