#!/usr/bin/env python3
import discord
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from dotenv import dotenv_values
from mal.anime import animes_season, search_anime

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

@slash.slash(name="anime")
async def reply_broadcast(ctx:SlashContext, anime:str):
    anime_info = search_anime(anime)
    if anime_info == None:
        await ctx.reply("No pude encontrar informacion de ese anime. uwu")
        return
    embed_message = discord.Embed()
    embed_message.title = anime_info.title
    embed_message = (embed_message
        .add_field(name="Score", value=anime_info.score)
        .add_field(name="Studio", value=anime_info.studio)
        .add_field(name="Episodes", value=anime_info.episodes)
        .add_field(name="Broadcast", value=anime_info.broadcast)
        .set_image(url=anime_info.image_url)
        )
    await ctx.reply(embed=embed_message)

client.run(config["DISCORD_TOKEN"])
