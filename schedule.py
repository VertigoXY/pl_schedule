import discord
import re
from discord.ext import commands


def import_schedule(f: str, s: list):
    with open(f) as file:
        for line in file.readlines():
            m = re.match(r"([a-zA-Z0-9 ]+: [a-zA-Z0-9 _-]+ vs [a-zA-Z0-9 ]+) ([0-9]+)", line)
            if m:
                s.append(m.group(1, 2))


class Schedule(commands.Cog):
    matches = list()

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        import_schedule("week1", self.matches)
        self.matches = sorted(self.matches, key=lambda k: k[1])

    @commands.command()
    async def nextgame(self, ctx: commands.Context):
        await ctx.send(f'The next game is {self.matches[0][0]}, on <t:{self.matches[0][1]}:F>.')

    @commands.command()
    @commands.is_owner()
    async def played(self, ctx: commands.Context):
        await ctx.send(f'Most recent game removed. Use $nextgame to check what is the newest next game.')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context):
        import_schedule("week1", self.matches)
        self.matches = sorted(self.matches, key=lambda k: k[1])
        await ctx.send(f'List of games updated.')


async def setup(bot: commands.Bot):
    await bot.add_cog(Schedule(bot))
