#!/usr/bin/env python3
import discord
from discord_slash import SlashCommand, SlashContext
from dotenv import dotenv_values
from mal.anime import animes_season
config = dotenv_values(".env")

client = discord.Client(intents=discord.Intents.default())
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@slash.slash(name="season")
async def reply_animes_season(ctx:SlashContext, limit:int = 5):
    await ctx.reply("Mostrando los {} animes con mas miembros en MyAnimeList".format(limit))
    for anime in animes_season(limit):
        embed_message = discord.Embed()
        embed_message.title = anime.title
        embed_message = (embed_message
            .add_field(name="Score", value=anime.score)
            .add_field(name="Episodes", value=anime.episodes)
            .add_field(name="Studio", value=anime.studio)
            .set_image(url=anime.image_url))

        await ctx.channel.send(embed=embed_message)

client.run(config["DISCORD_TOKEN"])
