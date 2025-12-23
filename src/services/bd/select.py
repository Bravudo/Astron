class select:
     
     def __init__(self,db):
           self.db = db

     async def user(self, discord_id: int):
            conn = await self.db.get_connection()
            try: 
                    query = """
                    SELECT * FROM usuario WHERE discord_id = $1 
                    """
                    user = await conn.fetchrow(query, discord_id)
                    if user is None:
                        print(f"check_user: Usuário não encontrado -> ID procurado: {discord_id}")
                        return None
                    
                    return user
            except Exception as e:
                print(f"ERRO 🟡 Usuário não existente ou erro no banco de dados: {e}")
            
     async def same_user_data(self, user_id:int):
        conn = await self.db.get_connection()
        try:
            query = "SELECT join_number FROM usuario WHERE discord_id = $1"
            number = await conn.fetchval(query, user_id)
            return int(number)
    
        except Exception as e:
            print(f'ERRO 🟡 Verificação de registro anteriormente: {e}')
            return None
        
     async def last_join_number(self):
            conn = await self.db.get_connection()
            try:
                    query = "select coalesce(max(join_number), 0) from usuario;"
                    last_number = await conn.fetchval(query)
                    return int(last_number) + 1
            except Exception as e:
                    print(f'ERRO 🟡 Busca de ultimo número: {e}')
                    return 1