import discord
from discord import app_commands
from discord.ext import commands
from src.views.newinserver import reduction_name, add_remove_rules,  add_member_roles, remove_member_roles 
from src.services.bloxlink import findroblox
from src.services.bd.config import check_last_number, check_same_data_user
from src.slash_commands.default import completed_symbol

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

