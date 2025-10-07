import discord
from discord.ext import commands
import sys

@commands.command()
@commands.has_permissions(administrator=True)
async def off(ctx):
    print('Bot Desligado por Comando')
    await ctx.send('Desligando...')
    await ctx.bot.close()
    raise sys.exit(0)

async def general_setup(bot):
    bot.add_command(off)