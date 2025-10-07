import mysql.connector
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
api_test = os.getenv("database_url")
db = mysql.connector.connect(
        host=os.getenv("database_url").split('@')[1].split(':')[0],
        port=os.getenv("database_url").split(':')[-1].split('/')[0],
        user=os.getenv("database_url").split('//')[1].split(':')[0],
        password=os.getenv("database_url").split(':')[2].split('@')[0],
        database=os.getenv("database_url").split('/')[-1]
)
cursor = db.cursor()
print(db)
    

async def save_db_new_user(ctx, dc_id, join_number, roblox_id, roblox_name, roblox_display):
    try:
        cursor.execute(f"INSERT INTO dc_user (dc_id, join_number, roblox_id, roblox_name, roblox_display) VALUES ({dc_id}, {join_number}, {roblox_id}, '{roblox_name}', '{roblox_display}')")
    except Exception as e:
        print(f'Erro: {e}')
        await ctx.send(f'ERRO: Verifique o terminal.')



@commands.command()
async def bd_log(ctx):
    print(f'API-TEST-1: {api_test}')
    await ctx.send('print bd')

async def bd_setup(bot):
    bot.add_command(bd_log)