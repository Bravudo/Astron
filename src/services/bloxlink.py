import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.embeds.registerlog import send_register_embed 
import os
import requests
load_dotenv()


registerlogchat = 1422434707416547500
api_key = os.getenv("blox_link_token")
roblox_user = "https://users.roblox.com/v1/usernames/users"


async def findroblox(ctx, member):
            
            guild_id = ctx.guild.id
            discord_id = member.id

            if isinstance(ctx, discord.Interaction):
             sender = ctx.response.send_message
             logchannel = ctx.guild.get_channel(registerlogchat)

            else:
                sender = ctx.send
                logchannel = ctx.guild.get_channel(registerlogchat)



            if member is None:
                await sender("Marque quem você quer procurar! Ex: !find @Tonhao")
                return

            if not api_key:
                await sender("Erro: chave da api não configurada")
            else: 
                try: 
                    url = f"https://api.blox.link/v4/public/guilds/{guild_id}/discord-to-roblox/{discord_id}"
                    headers = {"Authorization": api_key, "Accept": "application/json"}
                    response = requests.get(url, headers=headers, timeout=10)
                    print(response.json())
                    if response.status_code == 200: 
                        data = response.json()
                        roblox_id = data.get("robloxID")
                        roblox_username = data.get("robloxUsername")
                        if roblox_id:
                            roblox_response = requests.get(f"https://users.roblox.com/v1/users/{roblox_id}", timeout=10)
                            if roblox_response.status_code == 200:
                                roblox_data = roblox_response.json()
                                roblox_username = roblox_data.get("name")
                                roblox_displayname = roblox_data.get("displayName") 
                                print((f'id: {roblox_id}, user:{roblox_username}'))
                                await send_register_embed(
                                     logchannel, 
                                     member.id,
                                     join_number="000",
                                     roblox_id=roblox_id,
                                     roblox_username=roblox_username,
                                     roblox_displayname=roblox_displayname
                                )
                            else: 
                                 await sender(f'Erro Roblox: Busca não realizada')

                    elif response.status_code in [404,204]:
                        print((f'Usuário não vinculado ao BloxLink'))
                        print("URL chamada:", url)
                        print("Status:", response.status_code)
                        print("Conteúdo:", response.text)
                        await sender(f'Usuário não vinculado ao BloxLink.')
                    else:
                            await sender(f"Erro API: {response.status_code}")
                except requests.RequestException as e:
                        await sender(f"Erro no blox link: {e}")

@commands.command()
async def find(ctx, member: discord.Member = None):
    await findroblox(ctx, member)


async def bloxlink_setup(bot):
    bot.add_command(find)

        

