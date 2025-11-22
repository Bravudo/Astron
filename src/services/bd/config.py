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
        print('Conectado ao Banco Astryn')
        return conn

    except Exception as error:
        print(f'Erro na conexão com o banco: {error}')



#---------------TESTES---------------#
@commands.command()
@commands.has_permissions(administrator=True)
async def create_db(ctx):
    conn = await get_conn()
    try:
        if conn is None or conn.is_closed():
            await bd_connect()
        await conn.execute("""
        create table if not exists usuario (
                    id serial primary key,
                    discord_id bigint unique,
                    roblox_id bigint unique,
                    roblox_username text,
                    roblox_displayname text
                    );
        """)
        await conn.close()
        print('Tabela Criada')

    except Exception as e:
        print(f'Erro na criação da tabela user: {e}')


@commands.command()
@commands.has_permissions(administrator=True)
async def create_test_user(ctx):
    conn = await get_conn()
    try:
        if conn is None or conn.is_closed():
            await bd_connect()

        query = """
        INSERT INTO usuario (discord_id, roblox_id, roblox_username, roblox_displayname)
        values ($1, $2, $3, $4)
        """

        await conn.execute(query, 0,0,'BabyUser', 'BabyDisplay')
        print('usuario criado')
    except Exception as e:
        print(f'Erro ao criar usuário de teste: {e}')

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
async def delete_user_test(ctx, discord_id: int):
    conn = await get_conn()
    try:
        query = """
        DELETE FROM usuario WHERE discord_id = $1
        """
        await conn.execute(query, discord_id)
        await ctx.send(f'Usuário {discord_id} deletado')
    except Exception as e:
        print(f'Erro ao deletar o usuário')


async def bd_setup(bot):
    bot.add_command(bd_connect_c)
    bot.add_command(create_db)
    bot.add_command(create_test_user)
    bot.add_command(check_user)
    bot.add_command(delete_user_test)

