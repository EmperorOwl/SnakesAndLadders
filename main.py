""" Code for running the Discord bot. """

__author__ = "Ray Lin"
__date__ = "15/11/2022"
__modified__ = "14/12/2022"

import os
import time
import discord
from discord.ext import commands
from datetime import datetime

from game import GameAlreadyStarted
from discord_game import DiscordGame

bot = commands.Bot(command_prefix=commands.when_mentioned,
                   intents=discord.Intents.default())


@bot.tree.command(name='play', description="Start a game of Snakes & Ladders!")
async def play(interaction: discord.Interaction) -> None:
    """ Starts a game of Snakes & Ladders. """
    try:
        await DiscordGame(interaction).send_board(
            title="Welcome to Snakes & Ladders",
            description="Hit the button below to join!"
        )
    except GameAlreadyStarted:
        await interaction.response.send_message(
            f"{interaction.user.mention}! Only one game per channel. "
            f"Please `/finish` your current game."
        )


@bot.tree.command(name='ping', description="Check the ping.")
async def ping(interaction: discord.Interaction) -> None:
    """ Responds with the time it takes to send one message. """
    start = time.perf_counter()
    await interaction.response.send_message("Pinging...")
    end = time.perf_counter()
    await interaction.edit_original_response(
        content="Pong! {:.2f}ms".format((end - start) * 1000)
    )


@bot.tree.command(name='finish', description="Exit the current game.")
async def finish(interaction: discord.Interaction) -> None:
    """ Exits the current game by deleting the board. """
    os.remove(f'boards/{interaction.channel_id}.png')
    await interaction.response.send_message("Game Exited. Use `/play` to start "
                                            "a new one!")


@bot.command(name='sync', description="Sync the bot's slash commands.")
@commands.guild_only()
@commands.is_owner()
async def sync(context: commands.Context, location: str = 'this guild') -> None:
    """ Syncs the bot's slash commands with the Discord API. """
    if location == 'this guild':
        synced = await bot.tree.sync(guild=context.guild)
    elif location == 'global':
        synced = await bot.tree.sync()
    else:
        await context.send("Invalid location. Use `this guild` or `global`.")
        return
    if not synced:
        await context.send(f"Failed to sync any commands to {location}.")
    else:
        await context.send(f"Synced the following commands to {location}:\n" +
                           ', '.join([f"`{cmd.name}`" for cmd in synced]))


@bot.event
async def on_ready():
    """ Prints a message to indicate bot is online. """
    bot_start = datetime.now().strftime('%H:%M')
    print(f"Logged in as {bot.user.name} - {bot.user.id} - {bot_start}")
    # Removes all boards.
    for board in os.listdir('boards'):
        os.remove(f'boards/{board}')


bot.run(os.environ['DISCORD_BOT_TOKEN'])
