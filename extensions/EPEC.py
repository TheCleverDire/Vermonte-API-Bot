import discord
from discord import Member as DiscordMember
from discord.ext import commands
from discord.ext.commands import Bot, Greedy
from typing import Optional

class EPEC(commands.Cog):
    """E.P.E.C"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="giveme")
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def custom_role(self, ctx, *, role: discord.Role):
        """Add or remove custom role from user"""
        if role in ctx.author.roles:
            try:
                if ctx.author.top_role.name < ctx.get_role(626461345759494154).position:
                    await ctx.guild.remove_roles(role)
                else:
                    await ctx.send(user.mention + ", you cannot do that")
            except discord.Forbidden:
                await ctx.send("Could not remove " + user.name + "'s role")
            else:
                await ctx.send(user.name + " was removed from the role " + role.name)
        else:
            try:
                if ctx.author.roles.position < ctx.guild.get_role(626461345759494154).position:
                    await ctx.guild.add_roles(role)
                else: 
                    await ctx.send(user.mention + ", you cannot give yourself a role this high")
            except discord.Forbidden:
                await ctx.send("Could not add a role to " + user.name)
            else:
                await ctx.send(user.name + " was added to the role " + role.name)

    
def setup(bot):
    bot.add_cog(EPEC(bot))        