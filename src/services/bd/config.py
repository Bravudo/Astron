import mysql.connector
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
api_test = os.getenv("database_url")
print(api_test)
db = mysql.connector.connect(
    host=os.getenv("database_url").split('@')[1].split(':')[0],
    port=os.getenv("database_url").split(':')[-1].split('/')[0],
    user=os.getenv("database_url").split('//')[1].split(':')[0],
    password=os.getenv("database_url").split(':')[2].split('@')[0],
    database=os.getenv("database_url").split('/')[-1]
)
cursor = db.cursor()

@commands.command()
async def search_dc_user_db(ctx, discord_id):
    cursor.execute("SELECT dc_id, join_numebr, roblox_id, roblox_name, roblox_display FROM dc_user WHERE id = %s", ({discord_id},))
    user = cursor.fetchone()
    if user:
        dc_id, join_number, roblox_id, roblox_name, roblox_display = user
        print(user)


@commands.command()
async def bd_log(ctx):
    print(f'API-TEST-1: {api_test}')
    await ctx.send('print bd')

async def bd_setup(bot):
    bot.add_command(bd_log)
    bot.add_command(search_dc_user_db)