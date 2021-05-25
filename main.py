#!/usr/bin/env python3

import discord
from discord.ext import commands
import json
import time

with open("tokenfile", "r") as tokenfile: # defines the token so it knows how to get access to the bot
	token=tokenfile.read()

async def add_coins(user, amount): # define the function to add coins to a user's bank
	with open("coins.json", "r") as coinsraw:
		coins = json.loads(coinsraw.read())

	coins[str(user.id)] = amount

	with open("coins.json", "w") as coinsraw:
		coinsraw.write(json.dumps(coins))

intents = discord.Intents.all() # defines bot's intents
client = commands.Bot(command_prefix='o!', intents=intents) # defines the client and prefix

@client.event
async def on_ready():
	print("hello world!") # tells the console when the bot is online

@client.command(aliases=['c'])
async def claim(ctx): # the claim command that only works once
	with open("coins.json", "r") as coinsraw:
		coins = json.loads(coinsraw.read())

	if str(ctx.author.id) in coins:
		await ctx.send("you already got your 100 free Oni Coin:tm:")
		return
	else:
		await ctx.send("you got your first 100 Oni Coin:tm:! Congrats!")
		await add_coins(user=ctx.author, amount=100)

@client.command(aliases=['bal', 'balance', 'coin', 'amount', 'ch'])
async def check(ctx): # see the amount of coin you have
	with open("coins.json", "r") as coinsraw:
		coins = json.loads(coinsraw.read())

	try:
		await ctx.send(f"you have {coins[str(ctx.author.id)]} Oni Coin:tm:")
	except KeyError:
		await ctx.send("you havent done `o!claim` yet, do it to get 100 Oni Coin:tm: for free")

client.run(token) # runs the bot
