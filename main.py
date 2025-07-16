#!/usr/bin/env python3

import configparser
import os
import discord
from discord.ext import commands

from amazon import search_in_amazon
from watch import watch_background
from db import add_to_watchlist, get_watchlist, remove_from_watchlist

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
search_results = {}


# Commands
@bot.slash_command(name="wp_hello", description="Faire un hello world")
async def wp_hello(ctx):
    await ctx.respond("Hello world")

@bot.slash_command(name="wp_search", description="Effectuer une recherche sur Amazon")
async def wp_search(ctx, search_query=None):
    if not search_query:
        await ctx.respond("Veuillez spécifier une recherche.")
        return 
    await ctx.defer()
    message, results = search_in_amazon(search_query)
    if not results:
        await ctx.respond("Aucun résultat trouvé.")
        return
    search_results[ctx.user.id] = results
    await ctx.respond(message)

@bot.slash_command(name="wp_watchlist", description="Affiche la Watchlist")
async def wp_watchlist(ctx):
    items = get_watchlist(ctx.user.id)
    if not items:
        await ctx.respond("Votre watchlist est vide.")
        return
    message = "📦 Votre Watchlist :\n"
    for i, item in enumerate(items, 1):
        message += f"{i}. {item['title']} - {item['price']}\n"
    await ctx.respond(message)



@bot.slash_command(name="wp_watch", description="Ajoute un article à la Watchlist")
async def wp_watch(ctx, choice_number: int = None):
    if choice_number is None:
        await ctx.respond("Merci de préciser un numéro.")
        return

    index = choice_number - 1
    results = search_results.get(ctx.user.id, [])
    if index < 0 or index >= len(results):
        await ctx.respond("Numéro invalide.")
        return

    item = results[index]
    item["user_id"] = ctx.user.id
    add_to_watchlist(ctx.user.id, item)
    await ctx.respond(f"{item['title']} ajouté à votre liste de suivi.")

@bot.slash_command(name="wp_unwatch", description="Supprime un article de la Watchlist")
async def wp_unwatch(ctx, choice_number: int = None):
    if choice_number is None:
        await ctx.respond("Merci de préciser un numéro.")
        return
    index = choice_number - 1
    removed = remove_from_watchlist(ctx.user.id, index)
    if removed:
        await ctx.respond(f"{removed['title']} a été retiré de votre watchlist.")
    else:
        await ctx.respond("Numéro invalide.")

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    bot.loop.create_task(watch_background(bot))
    await bot.sync_commands()

bot.run(token)
