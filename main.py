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
search_results = {}
watch_list = {}


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
    message, search_results[ctx.user.id] = search(search_query)
    await ctx.respond(results)
     if not results:
        await ctx.respond("Aucun résultat trouvé.")
    else:
        await ctx.respond(message)

@bot.slash_command(name="wp_watchlist", description="Affiche la Watchlist")
async def wp_watchlist(ctx):
    user_list = watch_list.get(ctx.user.id, [])
    if not user_list:
        await ctx.respond("Votre Watchlist est vide.")
        return
    message = "Votre Watchlist :\n"
    for i, item in enumerate(user_list, 1):
        message += f"{i}. {item['title']} - {item['price']}\n"
    await ctx.respond(message)


@bot.slash_command(name="wp_watch", description="Ajoute un article à la Watchlist")
async def wp_watch(ctx, choice_number=None):
    user_id = ctx.user.id
    index = choice_number - 1
    user_search = search_results.get(user_id, [])
    if index < 0 or index >= len(user_search) or user_search[index] is None:
        await ctx.respond("Numéro invalide ou aucune recherche récente.")
        return
    article = user_search[index].copy()
    article["user_id"] = user_id
    if user_id not in watch_list:
        watch_list[user_id] = []
    watch_list[user_id].append(article)
    await ctx.respond(f'{article["title"]} ajouté à votre Watchlist')

@bot.slash_command(name="wp_unwatch", description="Supprime un article de la Watchlist")
async def wp_unwatch(ctx, choice_number=None):
    user_list = watch_list.get(ctx.user.id, [])
    index = choice_number - 1
    if index < 0 or index >= len(user_list):
        await ctx.respond("Numéro invalide.")
        return
    removed = user_list.pop(index)
    await ctx.respond(f'{removed["title"]} a été retiré de votre Watchlist')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    bot.loop.create_task(watch_background(bot, watch_list))
    await bot.sync_commands()

bot.run(token)
