import discord
from discord.ext import commands
from discord.ext.commands import Context
import traceback
import config
import os
import logging
import extensions.APIs

errors = ""
bot = commands.Bot(command_prefix=config.get_prefix, description=config.description)

if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in os.listdir("extensions") if os.path.isfile(os.path.join("extensions", f))]:
        try:
            bot.load_extension(config.cogDir + '.' + extension)
            logging.info(f'Loaded {extension}')
        except (discord.ClientException, ModuleNotFoundError):
            logging.error(f'Failed to load extension {extension}.', exc_info=True)

    @bot.event
    async def on_ready():
        info = await bot.application_info()
    
        logging.info(f'Logged in as: {bot.user.name} - {bot.user.id}')   
        logging.info(f'Owned by: {info.owner}')
        logging.info(f'Discord.py version: {discord.__version__}')

        activity = discord.Game("%help")
        await bot.change_presence(status=discord.Status.online, activity=activity)
        logging.info(f'Bots status succesfully set to %help')

    @bot.event
    async def on_message(message):
        #Check if message author is anothor bot if true then return    
        if message.author.bot:
            return
        ctx = await bot.get_context(message)
        if ctx.valid:
            await message.add_reaction("\N{HOURGLASS}")
            #Try to process command and if that fails log to console with reason
            try:    
                await bot.process_commands(message)
                logging.info(f'[command] - {message.author} ran command {message.content} in {message.guild.name}')
            except:
                logging.error(f'Bot has errored while processing the command: {message.content} in {message.guild.name}')
                           
            try:
                await message.remove_reaction("\N{HOURGLASS}", bot.user)
            except:
                pass


    bot.run(config.token, bot=True, reconnect=True)
