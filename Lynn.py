import discord
from discord.ext import commands
import traceback
import config
import os
import logging

errors = ""
bot = commands.Bot(command_prefix=config.get_prefix, description=config.description)

if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in os.listdir("extensions") if os.path.isfile(os.path.join("extensions", f))]:
        try:
            bot.load_extension(config.cogDir + '.' + extension)
        except (discord.ClientException, ModuleNotFoundError):
            logging.error(f'Failed to load extension {extension}.', exc_info=True)

    #Fires when bot is in ready state
    @bot.event
    async def on_ready():
        info = await bot.application_info()
    
        logging.info(f'Logged in as: {bot.user.name} - {bot.user.id}')   
        logging.info(f'Owned by: {info.owner}')
        logging.info(f'Discord.py version: {discord.__version__}')

    #Fires when the bot is invited/added to a guild
    @bot.event
    async def on_guild_join(guild):
        logging.info(f'I have just been invited to {guild.name} owned by {guild.owner}')

    #Fires when the bot leaves a guild
    @bot.event
    async def on_guild_remove(guild):
        logging.info(f'I have left {guild}, maybe I was either kicked or banned')

    #Fires when a message is sent in a channel
    @bot.event
    async def on_message(message):
        #Check if message author is anothor bot if true then return
        if message.author.bot:
            return
        #Check if E.P.E.C module is being called from its server
        if "E.P.E.C" in extension and not "626457668818567190" in message.guild.id:
            await message.send("Cannot use that module in this guild")
        else: 
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
