import discord
from discord import Intents, Status
from discord.ext import commands


bot = commands.Bot(command_prefix='$', intents=Intents.all(), status=Status.dnd)
cogs = ["schedule"]


async def setup_hook():
    for cog in cogs:
        await bot.load_extension(f"cogs.{cog}")

bot.setup_hook = setup_hook


@bot.listen()
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.is_owner()
async def reload(ctx: commands.Context, cog: str):
    if f'cogs.{cog}' in ctx.bot.extensions:
        await ctx.bot.reload_extension(f'cogs.{cog}')
        await ctx.send(f'Reloaded cog `{cog}`')
    else:
        await ctx.send(f'Cog `{cog}` not found.')

bot.run()
