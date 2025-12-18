import discord
from discord import app_commands
from discord.ext import commands
from src.views.newinserver import reduction_name, add_remove_rules,  add_member_roles, remove_member_roles 
from src.services.bloxlink import findroblox
from src.services.bd.config import check_last_number, check_same_data_user, check_user,remove_user
from src.slash_commands.default import completed_symbol

#Registro forçado via comando
class slash_register(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(
        name="registrar",
        description="Escolha um usuário e um número para forçar o registro"
    )
    @app_commands.describe(
        user="Selecione um usuário para o registro",
        number="Número de entrada dado ao usuário",
    )

    @commands.has_permissions(administrator=True)
    async def user_register(self,interaction: discord.Interaction, user: discord.Member, number:int | None = None):
        try:
            await interaction.response.defer(ephemeral=True)
            
            if number is None:
                number = await check_same_data_user(user.id)
            if number is None:
                number = await check_last_number()
        
            await findroblox(interaction, user, int(number))
            print(f'User Register - {user} - Número: {number}')

            #Se o usuário não existir, cria um novo
            num_str = str(number).zfill(2)
            apelido = user.display_name
            new_name = f"‹ {num_str} › ASR {apelido}" 
            new_name = await reduction_name(new_name)

            guild = interaction.guild
            await add_remove_rules(guild, user, add_member_roles, remove_member_roles)
            await user.edit(nick=new_name)
            await interaction.followup.send(f"{completed_symbol} <@{user.id}> Registrado!", ephemeral=True)

        except Exception as e:
            print(f'Erro ao registrar usuário utilizando /registrar: {e}')
            await interaction.followup.send(f"Erro ao registrar <@{user.id}>!", ephemeral=True)

class slash_check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="verificarregistro",
        description="Escolha um usuário para verificar no banco de dados"
    )
    @app_commands.describe(
        id="Selecione o ID do discord de um usuário para fazer a verificação."
    )
    @commands.has_permissions(administrator=True)
    async def user_check_id(self, interaction: discord.Interaction, id:str):
        await interaction.response.defer()
        try:
            int_id = int(id)
            user = await check_user(int_id)

            if user is None:
                await interaction.followup.send(f"❌ **Usuário não encontrado** -> ID Procurado: {id}")
                return
            
            await interaction.followup.send(f"💫 **Usuário Encontrado!** \n▶ ID: {int_id}\n▶ Entrada: {user['join_number']}")
            
        except Exception as e:
            print(f"ERRO ao verificar: {e}")

class slash_remove(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(
        name="removerregistro",
        description="Escolha um usuário para remover no banco de dados"
    )
    @app_commands.describe(
        id="Selecione o ID do discord de um usuário para fazer a remoção."
    )
    @commands.has_permissions(administrator=True)
    async def remover_user_id(self, interaction: discord.Interaction, id: str):
        await interaction.response.defer()
        try:
            int_id = int(id)
            remove = await remove_user(int_id)

            if remove is True:
                await interaction.followup.send(f"❌ **Usuário Removido**: {id}")
    
        except Exception as e:
            print(f"ERRO ao remover usuário: {e}")