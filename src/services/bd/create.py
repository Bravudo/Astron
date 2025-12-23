class create:
    def __init__(self,db):
           self.db = db

    async def user_table(self):
        try:
            conn = await self.db.get_connection()
        
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
                    print(f'ERRO 🔴 Criação da tabela user: {e}')
