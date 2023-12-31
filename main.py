#!/usr/bin/env python3

import configparser
import os
import discord
from discord.ext import commands

from amazon import search
from watch import watch_background


# Get Bot Token
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "bot.config"))
token = config.get("general","tokenBot")
guild_id = config.get("general","guildId")
channel_id = int(config.get("general","channelId"))

# Start Client
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix=('/'), intents=intents)

# Dict for storing results
search_results = []
watch_list = []


# Commands
@bot.slash_command(name="amazon_search", description="Effectuer une recherche sur Amazon", guilds_ids=[guild_id])
async def amazon_search(ctx, search_query=None):
    if search_query is not None:
        await ctx.defer()
        results = search(search_query, search_results)
        await ctx.respond(results)
        return
    await ctx.respond("Veuillez spécifier une recherche.")

@bot.slash_command(name="amazon_watchlist", description="Affiche la Watchlist", guilds_ids=[guild_id])
async def amazon_watchlist(ctx):
    message = "Votre Watchlist:\n"
    for i, result in enumerate(watch_list, 1):
        message += str(i) + " - " + str(result["title"]) + " - " + str(result["price"]) + "\n"
    await ctx.respond(f'{message}')

@bot.slash_command(name="amazon_watch", description="Ajoute un article à la Watchlist", guilds_ids=[guild_id])
async def amazon_watch(ctx, choice_number=None):
    index = int(choice_number) - 1
    if search_results[index] is None :
        await ctx.respond(f'Aucun résultat trouvé pour l\'ID {choice_number}')
        return
    watch_list.append(search_results[index])
    await ctx.respond(f'{search_results[index]["title"]} ajouté à la watchlist')

@bot.slash_command(name="amazon_unwatch", description="Supprime un article de la Watchlist", guilds_ids=[guild_id])
async def amazon_unwatch(ctx, choice_number=None):
    index = int(choice_number) - 1
    if watch_list[index] is None :
        await ctx.respond(f'Aucun résultat trouvé pour l\'ID {choice_number}')
        return
    title_to_remove = watch_list[index]["title"]
    watch_list.pop(index)
    await ctx.respond(f'{title_to_remove} retiré de la watchlist')


# Run the bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(watch_background(bot, watch_list, channel_id))
    await bot.sync_commands()

bot.run(token)
