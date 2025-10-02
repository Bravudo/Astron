import discord

async def send_register_embed(channel, user_id, join_number, roblox_id, roblox_username, roblox_displayname):
    user = await channel.guild.fetch_member(user_id)
    username = user.name

    embed = discord.Embed(
        title=f'Registro dos dados',
        description=f'{user.mention}',
        color=discord.Color.orange() 
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="Username", value=username, inline=True)
    embed.add_field(name="Entrada:", value=join_number, inline=True)
    embed.add_field(name="🌐Roblox", value="\u200b", inline=False)
    if roblox_id:
        embed.add_field(name="Username", value=roblox_username, inline=True)
        embed.add_field(name="Displayname", value=roblox_displayname, inline=True)
        embed.add_field(name="ID", value=roblox_id, inline=True)
    else:
        embed.add_field(name="🚫 Sem dados", value="\u200b", inline=False)
    
    await channel.send(embed=embed)