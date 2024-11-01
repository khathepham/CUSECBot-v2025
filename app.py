from flask import Flask
from infisical_sdk import InfisicalSDKClient
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="^", intent=intents)

@bot.command()
async def verify_member():
    pass

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    await bot.tree.sync()



bot.run()
