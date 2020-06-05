import discord
from discord.ext import commands
import config
import glob
import logging

errors = ''
bot = commands.Bot(command_prefix=config.get_prefix, description=config.description)

if __name__ == '__main__':
    for extension in [f.replace('.py', '').replace('/', '.') for f in glob.glob('cogs/**/*.py', recursive=True)]:
        try:
            bot.load_extension(extension)
        except (discord.ClientException, ModuleNotFoundError):
            logging.error(f'Failed to load extension {extension}.', exc_info=True)

    @bot.event
    async def on_ready():
        logging.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
        logging.info(f'Discord.py version: {discord.__version__}')

    @bot.event
    async def on_message(message):
        ctx = await bot.get_context(message)
        if ctx.valid:
            await ctx.channel.trigger_typing()
            await bot.process_commands(message)

    bot.run(config.token, bot=True, reconnect=True)