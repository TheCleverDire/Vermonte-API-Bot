import discord
import dateutil
from discord.ext import commands
from discord import CategoryChannel, Client, Colour, Embed, Guild, Member, Role, TextChannel, User, VoiceChannel, utils
from discord.ext.commands import Bot, BucketType, Cog, Context, command, group
import typing
import colorsys
from paginator import PaginatorSession

# Handles Commands/Events related to a Guilds Premium Features (Boosts etc)
class Premium(commands.Cog):
    """Premium (Boost) Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        if before.premium_subscription_count != after.premium_subscription_count:
            self.bot.get_guild(582647294831099930).get_channel(662061362972983366).send(before.name+" has just been boosted")
        if after.premium_tier == 1:
            self.bot.get_guild(582647294831099930).get_channel(662061362972983366).send("Congratulations"+before.name+" has just reached Tier 1")
        if after.premium_tier == 2:
            self.bot.get_guild(582647294831099930).get_channel(662061362972983366).send("Congratulations"+before.name+" has just reached Tier 2")
        if after.premium_tier == 3:
            self.bot.get_guild(582647294831099930).get_channel(662061362972983366).send("Congratulations"+before.name+" has just reached Max Tier 3")
        if after.premium_tier < before.premium_tier:
            self.bot.get_guild(582647294831099930).get_channel(662061362972983366).send("Bad luck"+before.name+" has just dropped a tier")

def setup(bot):
    bot.add_cog(Premium(bot))