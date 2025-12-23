import os
import asyncpg

from dotenv import load_dotenv
load_dotenv()

async def bd_connect():
    global conn
    try:
        db_url = os.getenv('database_url')
        conn = await asyncpg.connect(db_url)
        print('💫 - Conexão com Banco Astryn')
        return conn
    except Exception as error:
        print(f'ERRO 🔴 Conexão com o banco: {error}')

            