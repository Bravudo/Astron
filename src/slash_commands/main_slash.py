from src.slash_commands.register import slash_register

async def slash_commands_setup(bot):
    await bot.add_cog(slash_register(bot))