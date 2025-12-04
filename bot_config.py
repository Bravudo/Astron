import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
Initial_command = "$"
token = os.getenv("bot_token")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=f"{Initial_command}", intents=intents) 
