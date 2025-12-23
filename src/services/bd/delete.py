class delete:
        def __init__(self, db):
              self.db = db

        async def user(self, discord_id: int):
            conn = await self.db.get_connection()
            try: 
                    query = """
                    DELETE FROM usuario WHERE discord_id = $1 
                    """
                    await conn.fetchrow(query, discord_id)
                    return True
            
            except Exception as e:
                print(f"ERRO 🔴 Exclusão de usuário: {e}")