import discord
import re
from discord.ext import commands


def import_schedule(f: str, s: list):
    with open(f) as file:
        for line in file.readlines():
            m = re.match(r"([A-Z]{2}) ([a-zA-Z0-9 ]+: [a-zA-Z0-9 _-]+ vs [a-zA-Z0-9 ]+) ([0-9]+)", line)
            if m:
                s.append(m.group(1, 2, 3))


def is_authorized():
    async def predicate(ctx: commands.Context):
        return ctx.author.id in [531226728991817738, 496970908922150913]

    return commands.check(predicate)


class Schedule(commands.Cog):
    matches = list()
    teams = {
        "HH": "Hellfire Heatrans vs Hyperspace Horrors",
        "MR": "Metro Boomin' Megarays vs RPS Rhyperiors",
        "DT": "Drive-by Dragapults vs Trigger-Happy Thwackeys",
        "BP": "Big Baller Barraskewdas vs Playful Panchams"
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        import_schedule("week1", self.matches)
        self.matches = sorted(self.matches, key=lambda k: k[2])

    @commands.command()
    async def nextgame(self, ctx: commands.Context):
        await ctx.send(f'## {self.teams[self.matches[0][0]]}\n**{self.matches[0][1]}**\n<t:{self.matches[0][2]}:F>, <t:{self.matches[0][2]}:R>')

    @commands.command()
    @commands.is_owner()
    async def played(self, ctx: commands.Context):
        self.matches.pop(0)
        await ctx.send(f'Most recent game removed. Use $nextgame to check what is the newest next game.')

    @commands.command()
    async def allgames(self, ctx: commands.Context):
        text = ""
        for game in self.matches:
            text += f"- {game[1]} <t:{game[2]}:F>"
        await ctx.send(text)

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx: commands.Context):
        import_schedule("week1", self.matches)
        self.matches = sorted(self.matches, key=lambda k: k[2])
        await ctx.send(f'List of games updated.')


async def setup(bot: commands.Bot):
    await bot.add_cog(Schedule(bot))
