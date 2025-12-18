from src.slash_commands.register import slash_register,slash_check,slash_remove

async def slash_commands_setup(bot):
    await bot.add_cog(slash_register(bot))
    await bot.add_cog(slash_check(bot))
    await bot.add_cog(slash_remove(bot))