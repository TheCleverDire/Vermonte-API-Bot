import discord
from discord import Colour
from discord.ext import commands
from discord.ext.commands import Context
import logging
from Lynn import bot

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Fires when a user joins WishingMagic
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role = member.guild.get_role(681227473916395657)
        await member.add_roles(role, reason="On join role assign")
        logging.info(f'[Member Role Change] {role.name} was added to {member.name}')
        guild = member.guild
        wembed = discord.Embed(title="Member #"+str(len(guild.members)),
                               description=f"""Welcome {member.mention} to {guild.name}, be sure to check the rules. 
                               We hope you enjoy your time here.""")

        wembed.set_footer(text="Members: "+str(len(guild.members)))

        await guild.get_channel(681229226287824988).send(embed=wembed)

        logging.info(f'[Member Join] {member.name} joined {guild.name}')

        dmembed = discord.Embed(
            colour=Colour.blurple(),
            description=f"""
                {member.name},
                Thanks for joining WishingMagic
                
                The Staff at WishingMagic hopes you have a nicinge time with us.           
            """
        )

        await member.send(embed=dmembed)

def setup(bot):
    bot.add_cog(Events(bot))
    
