import discord
from discord.ext import commands
from discord import CategoryChannel, Colour, Embed, Guild, Member, Role, TextChannel, User, VoiceChannel, utils
from discord.ext.commands import Bot, BucketType, Cog, Context, command, group


class AdminInfo(commands.Cog):
    """Admin Info"""

    def __init__(self, bot):
        self.bot = bot
       
    @commands.command(name='invitations')
    @commands.has_permissions(view_audit_log=True)
    async def invite_list(self, ctx: Context) -> None:
        """Retrieves a list of active invites"""
        invit = ""
        invitations = await ctx.guild.invites()
        for invite in invitations:
            temp = "Max Age: " + str(invite["max_age"]) + "Code: " + str(invite["code"]) + "Guild: " + str(invite["guild"])
            invit += temp+ "\n"
            invitelist.append(invit)
            
        embed.discord.Embed(title="Invites", colour=Colour.blurple())
            
        for i in range(len(invitelist)):
            embed.add_field(name="Invite", value=invitelist[i])
    
        ctx.send(embed=embed)
       
       
       
    @commands.command(name='auditlog')
    @commands.has_permissions(view_audit_log=True)
    async def audit_log(self, ctx: Context) -> None:
        """Retrieves info from the audit log"""
        
        embed = discord.Embed(title="Auditlog", colour=Colour.blurple())
        
        async for entry in ctx.guild.audit_logs(limit=20):
            embed.add_field(name="---", value='{0.user} did {0.action} to {0.target}'.format(entry))

        await ctx.send(embed=embed)
        
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
        embed.set_footer(text=str(len(banlist)) + " Banned Users", icon_url="")
        
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