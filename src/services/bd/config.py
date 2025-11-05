import mysql.connector
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

save_on = True

load_dotenv()
api_test = os.getenv("database_url")

def check_connection():
    global db, cursor
    try:
        db.ping(reconnect=True, attempts=3, delay=2)
    except:
        db = mysql.connector.connect(
                host=os.getenv("database_url").split('@')[1].split(':')[0],
                port=os.getenv("database_url").split(':')[-1].split('/')[0],
                user=os.getenv("database_url").split('//')[1].split(':')[0],
                password=os.getenv("database_url").split(':')[2].split('@')[0],
                database=os.getenv("database_url").split('/')[-1]
        )
        cursor = db.cursor(dictionary=True)
        print("Reconectado ao banco")

    

async def save_db_new_user(dc_id, join_number, roblox_id, roblox_name, roblox_display):
        check_connection()
        global save_on
        try:
            cursor.execute(f"SELECT dc_id FROM dc_user WHERE dc_id = %s", (dc_id,))
            result = cursor.fetchone()
            if result:
                print('Teste: Usuario já existe')
                return
            
            cursor.execute(f"INSERT INTO dc_user (dc_id, join_number, roblox_id, roblox_name, roblox_display) VALUES ('{dc_id}', '{join_number}', '{roblox_id}', '{roblox_name}', '{roblox_display}')")
            print(f'Teste: Usuário inserido: {roblox_display}')
            #Salvar no Banco
            if save_on == True:
                db.commit()
        except Exception as e:
            print(f'Erro: {e}')


async def search_same_data_user(dc_id):
     check_connection()
     try:
        cursor.execute(f"SELECT join_number FROM dc_user WHERE dc_id = %s",(dc_id,))
        result = cursor.fetchone()
        if result:
            return result['join_number']
        else:
            return None
     except Exception as e:
        print(f'Erro: {e}')


async def search_last_number():
    check_connection()
    try:
        cursor.execute("SELECT MAX(join_number) as join_number FROM dc_user")
        result = cursor.fetchone()
        last = result['join_number'] or 0
        print(f'Ultimo número existente: {last}')
        return last + 1
    except Exception as e:
        print(f'Erro ao acessar o ultimo número de entrada: {e}')

@commands.command()
async def register_log(ctx):
    check_connection()
    try:
        cursor.execute("SELECT dc_id, join_number, roblox_id, roblox_name, roblox_display FROM dc_user")
        results = cursor.fetchall()

        if not results:
            await ctx.send("Nenhum registro encontrado.")
            return

        # Se vier como tupla (sem dictionary=True)
        for row in results:
            print(f"DC ID: {row['dc_id']} | Join#: {row['join_number']} | R ID: {row['roblox_id']} |Roblox: {row['roblox_name']} ({row['roblox_display']})")
        await ctx.send("Railway: Log Enviado")

    except Exception as e:
        print(f'Erro ao buscar registros: {e}')
        await ctx.send("Erro ao buscar dados do banco.")

@commands.is_owner()
@commands.command()
async def perm_bd_save(ctx):
    global save_on 
    if save_on == True:
        save_on = False
        print('Modo Atual: Temporariamente')
        await ctx.send("Modo Atual: Temporariamente")
    else:
        save_on = True
        print('Modo Atual: Permanentemente')
        await ctx.send("Modo Atual: Permanentemente")
        


@commands.command()
async def bd_log(ctx):
    print(f'API-TEST-1: {api_test}')
    await ctx.send('print api key')

async def bd_setup(bot):
    bot.add_command(bd_log)
    bot.add_command(view_register)
    bot.add_command(perm_bd_save)