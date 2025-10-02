import discord
from discord.ext import commands
import sys

id_log_channel = 1422434707416547500

@commands.command()
@commands.has_permissions(administrator=True)
async def off(ctx):
    await ctx.send('Desligando...')
    await ctx.bot.close()
    raise sys.exit(0)

@commands.command()
async def log_test(ctx):
    log_channel = ctx.bot.get_channel(id_log_channel)
    await log_channel.send('Log teste')


async def general_setup(bot):
    bot.add_command(off)
    bot.add_command(log_test)