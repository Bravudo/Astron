import os
import asyncpg
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
conn = None

@commands.command()
@commands.has_permissions(administrator=True)
async def bd_connect_c(ctx):
    await bd_connect()

#Criação da Váriavel Global para primeiro uso
async def get_conn():
    global conn
    if conn is None or conn.is_closed():
        conn = await bd_connect()
    return conn
        

#Conexão com o banco Astryn
async def bd_connect():
    global conn
    try:
        db_url = os.getenv('database_url')
        conn = await asyncpg.connect(db_url)
        print('💫 - Conexão com Banco Astryn')
        return conn
    except Exception as error:
        print(f'Erro na conexão com o banco: {error}')




@commands.command()
@commands.has_permissions(administrator=True)
async def create_user_db(ctx):
    conn = await get_conn()
    try:
        if conn is None or conn.is_closed():
            await bd_connect()
        await conn.execute("""
        create table if not exists usuario(
                    id serial primary key,
                    discord_id bigint unique,
                    join_number int unique,
                    roblox_id bigint unique,
                    roblox_username text,
                    roblox_displayname text
                    );
        """)
        print('Banco usuario criado')

    except Exception as e:
        print(f'Erro na criação da tabela user: {e}')





async def save_user(discord_id:int , join_number: int, roblox_id:int, roblox_username:str, roblox_displayname:str):
    conn = await get_conn()
    try:
        if roblox_id is None:
    
            query = """
            INSERT INTO usuario (discord_id, join_number)
            values ($1, $2)
            """
            await conn.execute(query, discord_id, join_number)
            print('Usuário salvo - DC')
        else:
            query = """
            INSERT INTO usuario (discord_id, join_number, roblox_id, roblox_username, roblox_displayname)
            values ($1, $2, $3, $4, $5)
            """
            await conn.execute(query, int(discord_id), int(join_number), int(roblox_id), str(roblox_username), str(roblox_displayname))
            print('Usuário salvo - DC + ROBLOX')
    except Exception as e:
        print(f'Erro ao criar usuário de teste: {e}')


async def check_last_number():
    conn = await get_conn()
    try:
            query = "select coalesce(max(join_number), 0) from usuario;"
            last_number = await conn.fetchval(query)
            return int(last_number) + 1
    except Exception as e:
            print(f'Erro ao buscar ultimo número: {e}')
            return 1


async def check_same_data_user(user_id:int):
    conn = await get_conn()
    try:
            query = "SELECT join_number FROM usuario WHERE discord_id = $1"
            number = await conn.fetchval(query, user_id)
            return int(number)
    
    except Exception as e:
            print(f'Erro verificar se o usuario já se registrou anteriormente: {e}')
            return None




@commands.command()
@commands.has_permissions(administrator=True)
async def check_user(ctx, discord_id: int):
    conn = await get_conn()
    try:

        query = """
        SELECT * FROM usuario WHERE discord_id = $1
        """
        result = await conn.fetchrow(query, discord_id)

        if result:
            await ctx.send(f"Usuário encontrado:\n```\n{result}\n```")
        else:
            await ctx.send(" Nenhum usuário econtrado")

    except Exception as e:
        print(f'Erro ao verificar usuário: {e}')
        await ctx.send(f"Ocorreu um erro: {e}")

@commands.command()
@commands.has_permissions(administrator=True)
async def delete_bd(ctx):
    conn = await get_conn()
    try:
        query = """
        DROP TABLE usuario
        """

        await conn.execute(query)
        print('Tabela Deletada')
        
    except Exception as e:
        print(f'Erro ao deletar o banco')


async def bd_setup(bot):
    bot.add_command(bd_connect_c)
    bot.add_command(create_user_db)
    bot.add_command(check_user)
    bot.add_command(delete_bd)
    print('Bd Setup: 🟩')

