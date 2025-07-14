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
@bot.slash_command(name="wp_hello", description="Faire un hello world")
async def wp_hello(ctx):
    await ctx.respond("Hello world")

@bot.slash_command(name="wp_search", description="Effectuer une recherche sur Amazon")
async def wp_search(ctx, search_query=None):
    if search_query is not None:
        await ctx.defer()
        results = search(search_query, search_results)
        await ctx.respond(results)
        return
    await ctx.respond("Veuillez spécifier une recherche.")

@bot.slash_command(name="wp_watchlist", description="Affiche la Watchlist")
async def wp_watchlist(ctx):
    message = "Votre Watchlist:\n"
    for i, result in enumerate(watch_list, 1):
        message += str(i) + " - " + str(result["title"]) + " - " + str(result["price"]) + "\n"
    await ctx.respond(f'{message}')

@bot.slash_command(name="wp_watch", description="Ajoute un article à la Watchlist")
async def wp_watch(ctx, choice_number=None):
    index = int(choice_number) - 1
    if search_results[index] is None :
        await ctx.respond(f'Aucun résultat trouvé pour l\'ID {choice_number}')
        return
    watch_list.append(search_results[index])
    await ctx.respond(f'{search_results[index]["title"]} ajouté à la watchlist')

@bot.slash_command(name="wp_unwatch", description="Supprime un article de la Watchlist")
async def wp_unwatch(ctx, choice_number=None):
    index = int(choice_number) - 1
    if watch_list[index] is None :
        await ctx.respond(f'Aucun résultat trouvé pour l\'ID {choice_number}')
        return
    title_to_remove = watch_list[index]["title"]
    watch_list.pop(index)
    await ctx.respond(f'{title_to_remove} retiré de la watchlist')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.run(token)
