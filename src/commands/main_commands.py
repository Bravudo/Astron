
#All Imports
from src.commands.utilities import utilities_setup

#Loading all Setups
async def commands_setup(bot):
    try:
        await utilities_setup(bot)

        
        print('🟦 - Setup Commands')
    except Exception as e:
        print(f'🟥 - Setup Commands')
        print(f'Erro em commands: {e}')