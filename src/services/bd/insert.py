

class insert:
    def __init__(self, db):
         self.db = db

    async def user(self, discord_id:int , join_number: int, roblox_id:int, roblox_username:str, roblox_displayname:str):
                conn = await self.db.get_connection()
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
                    print(f'ERRO 🟡 Criação de usuário: {e}')