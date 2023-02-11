""" Code for running the Discord bot. """

__author__ = "Ray Lin"
__date__ = "15/11/2022"
__modified__ = "11/02/2023"

import os
import json
import time
import discord
from discord.ext import commands
from datetime import datetime

from game import GameAlreadyStarted
from discord_game import DiscordGame

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=discord.Intents.default()
)


@bot.tree.command()
async def play(itx: discord.Interaction) -> None:
    """ Starts a game of Snakes & Ladders. """
    try:
        await DiscordGame(itx).send_board(
            title="Welcome to Snakes & Ladders",
            description="Hit the button below to join!"
        )
    except GameAlreadyStarted:
        await itx.response.send_message(
            f"{itx.user.mention}! Only one game per channel. "
            f"Please `/finish` your current game."
        )


@bot.tree.command()
async def ping(itx: discord.Interaction) -> None:
    """ Responds with the time it takes to send one message. """
    start = time.perf_counter()
    await itx.response.send_message("Pinging...")
    end = time.perf_counter()
    await itx.edit_original_response(
        content="Pong! {:.2f}ms".format((end - start) * 1000)
    )


@bot.tree.command()
async def finish(itx: discord.Interaction) -> None:
    """ Exits the current game. """
    os.remove(f'boards/{itx.channel_id}.png')
    await itx.response.send_message(
        "Game Exited. Use `/play` to start a new one!"
    )


@bot.command(name='sync', description="Sync the bot's slash commands.")
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    """ Syncs the bot's slash commands with the Discord API. """
    synced = await bot.tree.sync()
    if not synced:
        await ctx.send("Failed to sync any commands.")
    else:
        await ctx.send(f"Synced the following commands:\n" +
                       ', '.join([f"`{cmd.name}`" for cmd in synced]))


@bot.event
async def on_ready():
    """ Prints a message to indicate bot is online. """
    print(f"Logged in as {bot.user.name} - {bot.user.id} - "
          f"{datetime.now().strftime('%H:%M')}")
    # Removes all boards.
    for board in os.listdir('boards'):
        os.remove(f'boards/{board}')


with open('config.json', 'r') as f:
    bot.run(token=json.load(f)['token'], reconnect=True)
