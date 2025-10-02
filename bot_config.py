import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("bot_token")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents) 
