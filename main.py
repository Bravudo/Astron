import asyncio
from bot_config import bot, token
from src.commands.testcommands import general_setup
from src.views.newinserver import newpeople_setup
from src.services.bloxlink import bloxlink_setup
from src.services.bd.config import bd_setup



async def main():
    await general_setup(bot)
    await newpeople_setup(bot)
    await bloxlink_setup(bot)
    await bd_setup(bot)
    try:
        print('Presença: Online')
        await bot.start(token)
    except Exception as e:
        print(f'Erro ao inicializar o bot: {e}')

if __name__ == "__main__":
    asyncio.run(main())