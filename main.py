#!/usr/local/bin/python

import discord
from discord.ext import commands
import configparser

from scraping import *


# Get Bot Token
config = configparser.ConfigParser()
config.read('bot.config')
token = config.get('general','token')
guildId = config.get('general','guildId')

# Start Client
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('/'), intents=intents)

# Commands
@bot.slash_command(name='amazon_search', description='Effectuer une recherche sur Amazon')
async def amazon_search(ctx, search_query=None):
    if search_query is not None:
        results = search(search_query)
        await ctx.send(results)
    else:
        await ctx.send('Veuillez spécifier une recherche.')

@bot.slash_command(name='amazon_get', description="Récuperer un prix d'un article amazon", guilds_ids=[guildId])
async def amazon_get(ctx, url=None):
    if url is not None:
        price = get_price(url)
        await ctx.send(f'Le Prix de ton truc de merde: {price}')
    else:
        await ctx.send('Veuillez spécifier l\'URL.')

@bot.slash_command(name='amazon_watch', description="Définir une alerte sur le prix d'un article amazon", guilds_ids=[guildId])
async def amazon_watch(ctx, url=None, price=None):
    if url is not None and price is not None:
        watch_price(url, price)
        await ctx.send(f'Configuration réussie - URL : {url}, Prix : {price}')
    else:
        await ctx.send('Veuillez spécifier à la fois l\'URL et le prix.')

# Run
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Deploy slash commands
    await bot.sync_commands()

bot.run(token)
