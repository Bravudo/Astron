import discord
from discord.ext import commands
from src.services.bloxlink import findroblox


#Cargos de Entrada
#Retirar
noverify = 1420818499437330524

#Colocar
member = 1420643710961455175
verify = 1420859819950215278

add_member_roles = [member, verify]
remove_member_roles = [noverify]


class Register(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🌐", style=discord.ButtonStyle.primary, custom_id="register")
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        await interaction.response.defer(ephemeral=True)
        


        #Repassando a lista de cargos
        add_role = [guild.get_role(role_id) for role_id in add_member_roles]
        remove_role = [guild.get_role(role_id) for role_id in remove_member_roles]
        if add_role:
                await user.add_roles(*add_role) 
        if remove_role:
                await user.remove_roles(*remove_role)

        #Pesquisa sobre informações do roblox
        await findroblox(interaction, user)


@commands.command()
@commands.has_permissions(administrator=True)
async def register(ctx):
    view = Register()
    await ctx.send("Clique no botão para se Registrar!", view=view)



async def newpeople_setup(bot):
    bot.add_command(register)
    bot.add_view(Register())
