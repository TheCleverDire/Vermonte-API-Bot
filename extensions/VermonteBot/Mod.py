import discord
from discord.ext import commands
from discord import CategoryChannel, Colour, Embed, Guild, Member, Message, Role, TextChannel, User, VoiceChannel, utils
from discord.ext.commands import Bot, BucketType, Cog, Context, command, group

class Mod(commands.Cog):
    """Mod"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete')
    @commands.has_permissions(manage_messages=True)
    async def delete_message(self, ctx: Context, message: Message) -> None:
        """Deletes a given message"""
        await ctx.channel.fetch_message(message).delete()
        await ctx.send(f'Succesfully deleted message id: ' + message)
    

    @commands.command(name='purge', aliases=['prune'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int=None):
        """Purge an amount of messages in a channel"""
        if amount>500 or amount<0:
            raise commands.CommandError(message="Invalid amount")
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=amount)
        await ctx.send(f'Succesfully deleted **{int(amount)}** messages!', delete_after=5)

    @commands.command(name='echo', aliases=['say', 'repeat'])
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx, message):
        await ctx.message.delete()
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Mod(bot))
