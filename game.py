""" Code for running a game of Snakes & Ladders. """

__author__ = "Ray Lin"
__date__ = "15/11/2022"
__modified__ = "14/12/2022"

import os
from PIL import Image

from player import Player


class GameAlreadyStarted(Exception):
    """ Represents an error where a game of Snakes & Ladders has already been
    started.
    """
    pass


class Game:
    """ Represents a game of Snakes & Ladders.

    constants:
        MAX_NO_OF_PLAYERS: maximum number of players
        
    attributes:
        game_id: identification number of the game 
        index: current player 
        turns: number of rounds 
        players: list of players 

    """
    MAX_NO_OF_PLAYERS = 4

    def __init__(self, game_id: int) -> None:
        """ Creates a game of Snakes & Ladders. """
        self.game_id = game_id
        self.index = 0
        self.turns = 1
        self.players: list[Player] = []

    def check_game_already_started(self) -> None:
        """ Raises error if game has already started. """
        if f"{self.game_id}.png" in os.listdir('boards'):
            raise GameAlreadyStarted

    def check_player_already_joined(self, user_id: int) -> bool:
        """ Returns true if player has already joined the game. """
        return user_id in [player.id for player in self.players]

    def check_player_turn(self, user_id: int) -> bool:
        """ Returns true if it is the player's turn. """
        return self.players[self.index].id == user_id

    def check_player_win(self) -> bool:
        """ Returns true if there is a player at position 100. """
        for player in self.players:
            if player.pos == 100:
                return True
        return False

    def add_player(self, player: Player) -> None:
        """ Adds a player to the game. """
        self.players.append(player)

    def create_board_image(self) -> None:
        """ Updates the board image to reflect a player's move. """
        board = Image.open('resources/blank_board.png')

        sq_one_x = 31  # horizontal coordinate of square one
        sq_one_y = 442  # vertical coordinate of square one

        sq_ten_x = 441  # horizontal coordinate of square ten
        sq_ten_y = 442  # vertical coordinate of square ten

        one_sq_x = 45  # horizontal amount to move one square across
        one_sq_y = 45  # vertical amount to move one square up

        for player in self.players:
            if player.pos == 0:
                continue

            player_image = Image.open(f'resources/player{player.num}.png'
                                      ).convert('RGBA').resize((20, 20))
            diff = player.pos - 1
            x_diff = int(str(diff)[-1])
            y_diff = int(diff / 10)

            if (0 <= diff < 10) or (20 <= diff < 30) or (40 <= diff < 50) or \
                    (60 <= diff < 70) or (80 <= diff < 90):
                board_pos = (sq_one_x + x_diff * one_sq_x,
                             sq_one_y - y_diff * one_sq_y)
            else:
                board_pos = (sq_ten_x - x_diff * one_sq_x,
                             sq_ten_y - y_diff * one_sq_y)

            board.paste(player_image, board_pos, mask=player_image)

        board.save(f'boards/{self.game_id}.png')

    def delete_board_image(self) -> None:
        """ Removes PNG image of board. """
        os.remove(f'boards/{self.game_id}.png')


if __name__ == '__main__':
    from player import Player

    g = Game(game_id=1010)
    try:
        g.check_game_already_started()
    except GameAlreadyStarted:
        print("Successfully raised GameAlreadyStarted error")
        g.delete_board_image()
    g.create_board_image()
    p = Player(user_id=2020, user_name="Test Player", player_num=1)
    print(f"Player already joined: {g.check_player_already_joined(p.id)}")
    g.add_player(p)
    print(f"Player already joined: {g.check_player_already_joined(p.id)}")
    a = p.make_move()
    print(a)
    g.create_board_image()
    print(f"Player win: {g.check_player_win()}")
