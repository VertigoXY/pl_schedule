import discord
import re
from discord.ext import commands


def import_schedule(f: str, s: list):
    with open(f) as file:
        for line in file.readlines():
            m = re.match(r"([A-Z]{2}) ([a-zA-Z0-9 ]+: [a-zA-Z0-9 _-]+ vs [a-zA-Z0-9 _-]+) ([0-9]+)", line)
            if m:
                s.append(m.group(1, 2, 3))


class Schedule(commands.Cog):
    matches = list()
    teams = {
        "H": "Hellfire Heatrans",
        "R": "RPS Rhyperiors",
        "P": "Playful Panchams",
        "M": "Metro Boomin' Megarays",
        "D": "Drive-by Dragapults",
        "B": "Big Baller Barraskewdas",
        "T": "Trigger-Happy Thwackeys",
        "U": "Hyperspace Horrors"
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.deadline = ''

    @staticmethod
    async def auth(ctx: commands.Context):
        return ctx.author.id in [199748393721921537, 531226728991817738]

    @commands.command()
    async def nextgame(self, ctx: commands.Context):
        """Displays the next scheduled game."""
        await ctx.send(
            f'## {self.teams[self.matches[0][0][0]]} vs {self.teams[self.matches[0][0][1]]}\n**{self.matches[0][1]}**\n<t:{self.matches[0][2]}:F>, <t:{self.matches[0][2]}:R>')

    @commands.command()
    @commands.check(auth)
    async def addgames(self, ctx: commands.Context, *, games: str):
        games = games.strip("```\n").split('\n')
        for game in games:
            m = re.match(r"([A-Z]{2}) ([a-zA-Z0-9 ]+: [a-zA-Z0-9 _-]+ vs [a-zA-Z0-9 _-]+) ([0-9]+)", game)
            if m:
                self.matches.append(m.group(1, 2, 3))
            else:
                await ctx.send(f"Format non recognized: `{game}`")
                return
        self.matches = sorted(self.matches, key=lambda k: k[2])
        await ctx.send("Games added. Use $allgames to check the list.")

    @commands.command()
    @commands.check(auth)
    async def removegame(self, ctx: commands.Context, index: int):
        game = self.matches.pop(index - 1)
        self.matches = sorted(self.matches, key=lambda k: k[2])
        await ctx.send(f"Game removed: {game[1]}.")

    @commands.command()
    async def allgames(self, ctx: commands.Context):
        """Displays all the upcoming scheduled games."""
        text = ""
        for game in self.matches:
            text += f"- {game[1]} <t:{game[2]}:F>\n"
        text += f"- **DEADLINE** <t:{self.deadline}:F>\n"
        await ctx.send(text)

    @commands.command()
    @commands.is_owner()
    async def setdeadline(self, ctx: commands.Context, deadline: str):
        self.deadline = deadline
        await ctx.send(f"Deadline set. The deadline is <t:{deadline}:F>.")

    @commands.command()
    async def deadline(self, ctx: commands.Context):
        await ctx.send(f"**Deadline :** <t:{self.deadline}:F>")

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx: commands.Context):
        self.matches = list()
        import_schedule("week1", self.matches)
        self.matches = sorted(self.matches, key=lambda k: k[2])
        await ctx.send(f'List of games updated.')


async def setup(bot: commands.Bot):
    await bot.add_cog(Schedule(bot))
