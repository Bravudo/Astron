import asyncio
import discord
from discord.ext import commands
from src.services.bloxlink import findroblox
# from src.json.jsoncommands import load, save, file_name
from src.services.bd.config import check_last_number, check_same_data_user



#----Cargos-----#
#Retirar
noverify = 1420818499437330524

#Colocar
verify = 1420859819950215278

add_member_roles = [verify]
remove_member_roles = [noverify]
#---------------#
clanTag = "ASR"
locked_button = False





class Register(discord.ui.View):
    try:
        def __init__(self):
            super().__init__(timeout=None)
            

        @discord.ui.button(label="🌐", style=discord.ButtonStyle.primary, custom_id="register")
        async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
            global locked_button
            guild = interaction.guild
            user = interaction.user
            user_id = int(user.id)

            async def add_remove_rules(add, remove): 
                add_role = [guild.get_role(role_id) for role_id in add]
                remove_role = [guild.get_role(role_id) for role_id in remove]
                if add_role:
                    await user.add_roles(*add_role) 
                if remove_role:
                    await user.remove_roles(*remove_role)
                    return       
            
            if locked_button == True:
                await interaction.response.send_message("⏳ Aguarde! Outro usuário está se registrando. (10s)", ephemeral=True)
                return
            locked_button = True
                

        
            try:
                await interaction.response.defer(ephemeral=True)
                
                join_number = (await check_same_data_user(int(user_id)))
            
                #Se o usuário não existir, cria um novo
                if join_number == None:
                    join_number = int(await check_last_number())
                    if len(str(join_number)) == 1:
                        join_number_name = "0" + str(join_number)
                    apelido = user.display_name
                    new_name = f"‹ {join_number_name} › {clanTag} {apelido}"
                    
                    #Tamanho máximo de nome
                    if len(new_name) > 32:
                        new_name = new_name[:32]
                        
                    await user.edit(nick=new_name)
                    
                #Se o usuario já existir, utiliza as informações da primeira pesquisa
                else:
                    apelido = user.display_name
                    if len(str(join_number)) == 1:
                        join_number_name = "0" + str(join_number)


                    new_name = f"‹ {join_number_name} › {clanTag} {apelido}"
                    if len(new_name) > 32:
                        new_name = new_name[:32]
                    await user.edit(nick=new_name)
                    await add_remove_rules(add_member_roles, remove_member_roles)
                    return

                await add_remove_rules(add_member_roles, remove_member_roles)
                #Pesquisa sobre informações do roblox
                await findroblox(interaction, user, int(join_number))
            except Exception as e:
                print(f'Erro ao se registrar: {e}')
            finally:
                await asyncio.sleep(10)
                locked_button = False
    except Exception as e:
        print(f'Erro ao tentar spawnar o botão: {e}')


@commands.command()
@commands.has_permissions(administrator=True)
async def register(ctx):
    view = Register()
    await ctx.send("Clique no botão para se Registrar!", view=view)



async def newpeople_setup(bot):
    bot.add_command(register)
    bot.add_view(Register())
