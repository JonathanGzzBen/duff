#!/usr/bin/env python3
import discord
from discord import embeds
from discord.channel import TextChannel
from dotenv import dotenv_values
from mal.anime import animes_season
config = dotenv_values(".env")

class DuffClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    
    async def on_message(self, message: discord.Message):
        if message.author == client.user:
            return
        if str(message.content).startswith("animes de la season"):
            await self.reply_animes_season(message)
    
    async def reply_animes_season(self, message: discord.Message):
        await message.reply("Mostrando los 5 animes con mas miembros en MyAnimeList")
        for anime in animes_season(limit=5):
            embed_message = discord.Embed()
            embed_message.title = anime.title
            embed_message = (embed_message
                .add_field(name="Score", value=anime.score)
                .add_field(name="Episodes", value=anime.episodes)
                .add_field(name="Studio", value=anime.studio)
                .set_image(url=anime.image_url))

            await message.channel.send(embed=embed_message)
    

client = DuffClient()
client.run(config["DISCORD_TOKEN"])
