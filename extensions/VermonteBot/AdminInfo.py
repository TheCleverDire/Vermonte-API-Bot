import discord
from discord.ext import commands
from discord import CategoryChannel, Colour, Embed, Guild, Member, Role, TextChannel, User, VoiceChannel, utils
from discord.ext.commands import Bot, BucketType, Cog, Context, command, group


class AdminInfo(commands.Cog):
    """Admin Info"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='banlist', aliases=['blist'])
    @commands.is_owner()
    @commands.has_permissions(ban_members=True, administrator=True)
    async def banlist(self, ctx: Context) -> None:
        """Retrieves a list of Banned Members as raw output"""
        banlist = await ctx.guild.bans()
        
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Banned Users**
                {banlist}
            """
        )
        
        await ctx.send(embed=embed)
        
    
    
    @commands.command(name='invites', aliases=['inv'])
    @commands.is_owner()
    @commands.has_permissions(manage_guild=True, administrator=True)
    async def invites(self, ctx: Context) -> None:
        """Retrieves a list of invites as raw output"""
        invitelist = await ctx.guild.invites()
        
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Invites**
                {invitelist}
            """
        )
        
        await ctx.send(embed=embed)    
        

def setup(bot):
    bot.add_cog(AdminInfo(bot))