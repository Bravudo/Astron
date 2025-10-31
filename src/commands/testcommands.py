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

copiada = {}


@commands.command()
@commands.has_permissions(administrator=True)
async def copiar(ctx, message_id: int):
    try:
        canal = ctx.channel
        msg = await canal.fetch_message(message_id)

        dados = {
            "content": msg.content,
            "embeds": [e.to_dict() for e in msg.embeds],
            "attachments": [a.url for a in msg.attachments]
        }

        copiada[ctx.author.id] = dados
        await ctx.message.add_reaction("✅")  

    except Exception as e:
        await ctx.reply(f"ERRO: {e}")
        print (f'ERRO COPIANDO A MENSAGEM: {e}')


@commands.command()
@commands.has_permissions(administrator=True)
async def colar(ctx):
    if ctx.author.id not in copiada:
        await ctx.reply("Nenhuma mensagem copiada ainda.")
        return

    dados = copiada[ctx.author.id]
    embeds = [discord.Embed.from_dict(e) for e in dados["embeds"]]

    arquivos = []
    for url in dados["attachments"]:
        arquivo = await discord.File.from_url(url)
        arquivos.append(arquivo)

    await ctx.send(content=dados["content"], embeds=embeds, files=arquivos)

async def general_setup(bot):
    bot.add_command(off)
    bot.add_command(copiar)
    bot.add_command(colar)