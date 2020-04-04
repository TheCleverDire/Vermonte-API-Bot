import discord
from discord.ext import commands
from discord import CategoryChannel, Colour, Embed, Guild, Member, Role, TextChannel, User, VoiceChannel, utils
from discord.ext.commands import Bot, BucketType, Cog, Context, command, group
from datetime import datetime


class AdminInfo(commands.Cog):
    """Admin Info"""

    def __init__(self, bot):
        self.bot = bot
       
    @commands.command(name='invitelist')
    @commands.has_permissions(view_audit_log=True)
    async def invite_list(self, ctx: Context) -> None:
        """Retrieves a list of invites"""        
        invites = sorted(await ctx.guild.invites(), key=lambda invite: invite.created_at)
        
        invite_string = ""
        for invite in invites:
            invite_string += f"Url: {invite.url} - Inviter: {invite.inviter} - Uses: {invite.uses} - Max Uses: {invite.max_uses} - Temporary: {invite.temporary}"
       
        embed = discord.Embed(title="Invites", colour=Colour.blurple(), description=f"""{invite_string}""")

        await ctx.send(embed=embed)
       
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

    @commands.command(name="msghist")
    @commands.has_permissions(manage_messages=True)
    async def msg_history(self, ctx, *, channel: discord.TextChannel):
        """Retrieves Message History"""
        messages = await channel.history(limit=123).flatten()

        f = open("logs/message/"+datetime.now().strftime('%Y-%m-%d')+".json", "x+")
        f.write(str(messages))
        f.close()        

def setup(bot):
    bot.add_cog(AdminInfo(bot))