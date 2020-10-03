import discord
import random
from discord.ext import commands

class Random(commands.Cog):
    '''Random'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dice', aliases=['die'])
    async def dice(self, ctx, *, args='1d6'):
        """Rolls n dice with set amount of faces. For example:
        1d6 = 1 dice with 6 faces.
        2d10 = 2 dices with 10 faces each."""
        if not 'd' in args:
            n = int(args)
            f = 6
        else:
            n = int(args.split('d')[0])
            f = int(args.split('d')[1])

        if n == 0:
            await ctx.send('You roll 0 dice. Nothing happens.')
            return
        if f == 0:
            await ctx.send(f"You roll {n} {'dice' if n > 1 else 'die'} with 0 faces. The world implodes as your zero-dimensional {'dice' if n > 1 else 'die'} hit the table.")
            return
        
        if f < 0:
            await ctx.send(f"You try to roll {n} {'dice' if n > 1 else 'die'} with negative faces, but you realize that you're all out of negative-dimensional dice.")
            return
        if n < 0:
            roll = random.randint(abs(n), abs(n)*f)
            await ctx.send(f"You roll negative {n} dice. The dice jump from the table back into your hand. You rolled **{roll}**!")
            return

        roll = random.randint(n, n*f)
        await ctx.send(f"You roll {n} {'dice' if n > 1 else 'die'} with {f} face{'s' if f > 1 else ''}. You rolled **{roll}**!")



def setup(bot):
    bot.add_cog(Random(bot))
