from src.services.bd.delete import delete
from src.services.bd.insert import insert
from src.services.bd.select import select
from src.services.bd.create import create
from src.services.bd.connect import bd_connect

class Database:
    def __init__(self):
         self.conn = None
         self.insert = insert(self)
         self.select = select(self)
         self.delete = delete(self)
         self.create = create(self)

    async def get_connection(self):
            if self.conn is None or self.conn.is_closed():
                self.conn = await bd_connect()
            return self.conn

async def database_setup(bot):
    try:
        db = Database()
        print('🟦 - Setup Database')
    except Exception as e:
        print(f'🟥 - Setup Database')
        print(f'ERRO 🔴 Erro ao carregar setup do banco de dados: {e}')
         

