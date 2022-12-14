""" Code for running a game of Snakes & Ladders in Discord. """

__author__ = "Ray Lin"
__date__ = "15/11/2022"
__modified__ = "14/12/2022"

import asyncio
import discord
from discord import ButtonStyle
from discord import Interaction
from discord import Embed, File
from discord import Colour
from discord.ui import View, Button

from game import Game
from player import Player


class DiscordGame(View, Game):
    """ Represents the Snakes & Ladders game via Discord UI buttons.

    constants:
        MAX_NO_OF_PLAYERS: maximum number of players (inherited from Game)
        DELAY_BETWEEN_TURNS: time (s) to wait before beginning next turn

    attributes:
        children: list of buttons (inherited from View)
        buttons: copy of children
        interaction: original interaction
        game_id: identification number of the game (inherited from Game)
        index: current player (inherited from Game)
        turns: number of rounds (inherited from Game)
        players: list of players (inherited from Game)

    buttons:
        0: corresponds to the index of the Join button
        1: corresponds to the index of the Start button
        2: corresponds to the index of the Roll button
        (i.e. in the order they are defined in this class)

    """
    DELAY_BETWEEN_TURNS = 5

    def __init__(self, interaction: Interaction):
        """ Creates a game of Snakes & Ladders using Discord UI. """
        View.__init__(self)
        Game.__init__(self, game_id=interaction.channel_id)
        self.check_game_already_started()  # Raises GameAlreadyStarted error.
        self.buttons = self.children
        self.interaction = interaction
        self.clear_items()  # Remove all buttons.
        self.add_item(self.buttons[0])  # Add join button.
        self.create_board_image()

    async def send_board(self, title: str, description: str) -> None:
        """ Messages an embed with dynamic title and description and current
        status of the board as an image.
        """
        embed = Embed(title=title, description=description, colour=Colour.blue())
        file = File(fp=f"boards/{self.game_id}.png", filename="board.png")
        embed.set_image(url="attachment://board.png")
        try:
            await self.interaction.response.send_message(embed=embed,
                                                         file=file,
                                                         view=self)
        except discord.errors.InteractionResponded:
            await self.interaction.edit_original_response(embed=embed,
                                                          attachments=[file],
                                                          view=self)

    @discord.ui.button(label='Join the game!', style=ButtonStyle.primary)
    async def join(self, interaction: Interaction, button: Button):
        """ Manages the join button. """
        if self.check_player_already_joined(interaction.user.id):
            await interaction.response.send_message(
                content=f"{interaction.user.mention}! You have already joined!",
                ephemeral=True
            )
            return
        # Otherwise, add new player.
        self.add_player(Player(user_id=interaction.user.id,
                               user_name=interaction.user.display_name,
                               player_num=len(self.players) + 1))
        # Prepare list of players.
        player_info = '\n'.join([f"Player {num} - {name}" for num, name in zip(
            [p.num for p in self.players], [p.name for p in self.players])])
        # Add start button when number of players is greater than 1.
        if len(self.players) > 1:
            self.add_item(self.buttons[1])
        # Remove join button when number of players is maximum.
        if len(self.players) == Game.MAX_NO_OF_PLAYERS:
            self.clear_items()
            self.add_item(self.buttons[1])
        # Update board.
        await self.send_board(title="Welcome to Snakes & Ladders",
                              description=f"```{player_info}```")
        # Fake respond to user to prevent "This interaction failed" error.
        await interaction.response.edit_message()

    @discord.ui.button(label='Start the game!', style=ButtonStyle.success)
    async def start(self, interaction: Interaction, button: Button):
        """ Manages the start button. """
        self.clear_items()  # Remove all buttons.
        self.add_item(self.buttons[2])  # Add roll button.
        # Update board.
        await self.send_board(
            title=f"Turn #{self.turns}",
            description=f"{self.players[self.index].name}, its your turn!"
        )
        # Fake respond to user to prevent "This interaction failed" error.
        await interaction.response.edit_message()

    @discord.ui.button(label="Roll the dice!", style=ButtonStyle.primary)
    async def roll(self, interaction: Interaction, button: Button):
        """ Manages the roll button. """
        if not self.check_player_turn(interaction.user.id):
            await interaction.response.send_message(
                content=f"{interaction.user.mention}! It's not your turn!",
                ephemeral=True)
            return
        # Fake respond to user to prevent "This interaction failed" error.
        await interaction.response.edit_message()
        # Remove roll button to prevent double tap.
        self.clear_items()
        # Perform user's turn and update board.
        move = self.players[self.index].make_move()
        self.create_board_image()
        await self.send_board(title=f"Turn #{self.turns}",
                              description=move)
        await asyncio.sleep(5)  # Allow some time for user to comprehend move.
        # Check winner.
        if self.check_player_win():
            await self.send_board(
                title=f"Turn #{self.turns}",
                description=f"{self.players[self.index].name} is the winner!"
            )
            self.delete_board_image()
            self.stop()
            return
        # Increment player index and round counter.
        self.index = (self.index + 1) % len(self.players)
        self.turns += 1
        # Begin next turn.
        self.add_item(self.buttons[2])  # Add roll button.
        await self.send_board(
            title=f"Turn #{self.turns}",
            description=f"{self.players[self.index].name}, its your turn!"
        )
