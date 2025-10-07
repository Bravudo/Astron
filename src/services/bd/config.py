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
    

async def save_db_new_user(dc_id, join_number, roblox_id, roblox_name, roblox_display):
    try:
        cursor.execute(f"INSERT INTO dc_user (dc_id, join_number, roblox_id, roblox_name, roblox_display) VALUES ('{dc_id}', '{join_number}', '{roblox_id}', '{roblox_name}', '{roblox_display}')")
    except Exception as e:
        print(f'Erro: {e}')

@commands.command()
async def view_register(ctx):
    try:
        cursor.execute("SELECT * FROM dc_user")
        results = cursor.fetchall()
        
        if not results:
            print("Nenhum registro encontrado.")
            await ctx.send("Nenhum registro encontrado no banco de dados.")
            return

        # Exibe via print no console
        for row in results:
            print(f"DC ID: {row['dc_id']} | Join#: {row['join_number']} | Roblox: {row['roblox_name']} ({row['roblox_display']})")

        # E também manda um resumo no Discord
        msg = "\n".join([f"{r['roblox_name']} ({r['roblox_display']})" for r in results])
        await ctx.send(f"**Registros encontrados:**\n{msg}")
    except Exception as e:
        print(f'Erro: {e}')

@commands.command()
async def bd_log(ctx):
    print(f'API-TEST-1: {api_test}')
    await ctx.send('print bd')

async def bd_setup(bot):
    bot.add_command(bd_log)
    bot.add_command(view_register)