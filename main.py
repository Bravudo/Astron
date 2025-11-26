import asyncio
from bot_config import bot, token
from src.commands.testcommands import general_setup
from src.views.newinserver import newpeople_setup
from src.services.bloxlink import bloxlink_setup
from src.services.bd.config import bd_setup
from src.slash_commands.main_slash import slash_commands_setup



async def main():
    await slash_commands_setup(bot)
    await general_setup(bot)
    await newpeople_setup(bot)
    await bloxlink_setup(bot)
    await bd_setup(bot)
    try:
        
        await bot.start(token)
    except Exception as e:
        print(f'Erro ao inicializar o bot: {e}')

@bot.event
async def on_ready():
    try:
            await bot.tree.sync()
            print('Slash Commands Setup: 🟩')
    except Exception as e:
        print(f'Erro ao carregar slash commands: {e}')         
    print('⭐ Bot Online ⭐ ')

if __name__ == "__main__":
    asyncio.run(main())