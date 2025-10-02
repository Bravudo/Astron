import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
load_dotenv()

api_key = os.getenv("blox_link_token")
roblox_user = "https://users.roblox.com/v1/usernames/users"

@commands.command(name="find")
async def find(ctx, member: discord.Member = None, username_fallback: str = None):
            if member is None:
                await ctx.send("Marque quem você quer procurar! Ex: !find @Tonhao")
                return

            guild_id = ctx.guild.id
            discord_id = member.id

            if not api_key:
                await ctx.send("Erro: chave da api não configurada")
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
                                await ctx.send(f"Blox Link\nID: {roblox_id}\nDisplayname: {roblox_displayname}\nUser: {roblox_username}")
                            else: 
                                 await ctx.send(f'Erro Roblox: Busca não realizada')

                    elif response.status_code in [404,204]:
                        print((f'Usuário não vinculado ao BloxLink'))
                        print("URL chamada:", url)
                        print("Status:", response.status_code)
                        print("Conteúdo:", response.text)
                        await ctx.send(f'Usuário não vinculado ao BloxLink.')
                    else:
                            await ctx.send(f"Erro API: {response.status_code}")
                except requests.RequestException as e:
                        await ctx.send(f"Erro no blox link: {e}")


async def bloxlink_setup(bot):
    bot.add_command(find)

        

