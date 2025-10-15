import discord

RobloxIcon = "<:roblox:1423390785482784849>"
DiscordIcon = "<:discord:1423392381910253638>"


async def send_register_embed(channel, user_id, join_number, roblox_id, roblox_username, roblox_displayname):
    user = await channel.guild.fetch_member(user_id)
    username = user.name

    embed = discord.Embed(
        title=f'Registro Astryn',
        description=f'{user.mention}',
        color=discord.Color.from_rgb(255, 255, 255) 
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name=f"{DiscordIcon} Username", value=username, inline=True)
    embed.add_field(name=f"{DiscordIcon} Entrada", value=join_number, inline=True)
    embed.add_field(name=f"{DiscordIcon} ID", value=user_id, inline=True)

    if roblox_id == 'None':
        embed.add_field(name=f"{RobloxIcon} Sem dados Roblox 🚫", value="\u200b", inline=True)
    else:
        embed.add_field(name=f"{RobloxIcon} Username", value=roblox_username, inline=True)
        embed.add_field(name=f"{RobloxIcon} Displayname", value=roblox_displayname, inline=True)
        embed.add_field(name=f"{RobloxIcon} ID", value=roblox_id, inline=True)
        
    await channel.send(embed=embed)