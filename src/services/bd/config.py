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
cursor = db.cursor(dictionary=True)
print(db)
    

async def save_db_new_user(dc_id, join_number, roblox_id, roblox_name, roblox_display):
    try:
        cursor.execute(f"INSERT INTO dc_user (dc_id, join_number, roblox_id, roblox_name, roblox_display) VALUES ('{dc_id}', '{join_number}', '{roblox_id}', '{roblox_name}', '{roblox_display}')")
        #db.commit() PARA SALVAR OS DADOS INSERIDOS
    except Exception as e:
        print(f'Erro: {e}')

async def search_same_data_user(dc_id):
     try:
        cursor.execute(f"SELECT join_number from dc_user WHERE dc_id = %s",(dc_id,))
        result = cursor.fetchone()
        if result:
            return result['join_number']
        else:
            return None
     except Exception as e:
        print(f'Erro: {e}')


async def search_last_number():
    try:
        cursor.execute("SELECT MAX(join_number) as join_number FROM dc_user")
        result = cursor.fetchone()
        last = result['join_number'] or 0
        print(f'Ultimo número existente: {last}')
        return last + 1
    except Exception as e:
        print(f'Erro ao acessar o ultimo número de entrada: {e}')

@commands.command()
async def view_register(ctx):
    try:
        cursor.execute("SELECT dc_id, join_number, roblox_id, roblox_name, roblox_display FROM dc_user")
        results = cursor.fetchall()

        if not results:
            await ctx.send("Nenhum registro encontrado.")
            return

        # Se vier como tupla (sem dictionary=True)
        for row in results:
            print(f"DC ID: {row['dc_id']} | Join#: {row['join_number']} | Roblox: {row['roblox_name']} ({row['roblox_display']})")

        await ctx.send("Console railway")

    except Exception as e:
        print(f'Erro ao buscar registros: {e}')
        await ctx.send("Erro ao buscar dados do banco.")

@commands.command()
async def bd_log(ctx):
    print(f'API-TEST-1: {api_test}')
    await ctx.send('print bd')

async def bd_setup(bot):
    bot.add_command(bd_log)
    bot.add_command(view_register)