""" Code for a player in the Snakes & Ladders game. """

__author__ = "Ray Lin"
__date__ = "15/11/2022"
__modified__ = "14/12/2022"

import random


class Player:
    """ Represents a Snakes & Ladders player.

    constants:
        BOARD: numeric board to look up location of the snakes and the ladders
        DICE_MIN: minimum number to roll on the die
        DICE_MAX: maximum number to roll on the die

    attributes:
        user_id: identification number of the user
        user_name: name of the user
        player_num: in-game number of the player
        player_pos: in-game position of the player
    """

    BOARD = [
        {"pos": "0", "move": ""},
        {"pos": "1", "move": "38"},
        {"pos": "2", "move": ""},
        {"pos": "3", "move": ""},
        {"pos": "4", "move": "14"},
        {"pos": "5", "move": ""},
        {"pos": "6", "move": ""},
        {"pos": "7", "move": ""},
        {"pos": "8", "move": "30"},
        {"pos": "9", "move": ""},
        {"pos": "10", "move": ""},
        {"pos": "11", "move": ""},
        {"pos": "12", "move": ""},
        {"pos": "13", "move": ""},
        {"pos": "14", "move": ""},
        {"pos": "15", "move": ""},
        {"pos": "16", "move": ""},
        {"pos": "17", "move": ""},
        {"pos": "18", "move": ""},
        {"pos": "19", "move": ""},
        {"pos": "20", "move": ""},
        {"pos": "21", "move": "42"},
        {"pos": "22", "move": ""},
        {"pos": "23", "move": ""},
        {"pos": "24", "move": ""},
        {"pos": "25", "move": ""},
        {"pos": "26", "move": ""},
        {"pos": "27", "move": ""},
        {"pos": "28", "move": "76"},
        {"pos": "29", "move": ""},
        {"pos": "30", "move": ""},
        {"pos": "31", "move": ""},
        {"pos": "32", "move": "10"},
        {"pos": "33", "move": ""},
        {"pos": "34", "move": ""},
        {"pos": "35", "move": ""},
        {"pos": "36", "move": "6"},
        {"pos": "37", "move": ""},
        {"pos": "38", "move": ""},
        {"pos": "39", "move": ""},
        {"pos": "40", "move": ""},
        {"pos": "41", "move": ""},
        {"pos": "42", "move": ""},
        {"pos": "43", "move": ""},
        {"pos": "44", "move": ""},
        {"pos": "45", "move": ""},
        {"pos": "46", "move": ""},
        {"pos": "47", "move": ""},
        {"pos": "48", "move": "26"},
        {"pos": "49", "move": ""},
        {"pos": "50", "move": "67"},
        {"pos": "51", "move": ""},
        {"pos": "52", "move": ""},
        {"pos": "53", "move": ""},
        {"pos": "54", "move": ""},
        {"pos": "55", "move": ""},
        {"pos": "56", "move": ""},
        {"pos": "57", "move": ""},
        {"pos": "58", "move": ""},
        {"pos": "59", "move": ""},
        {"pos": "60", "move": ""},
        {"pos": "61", "move": ""},
        {"pos": "62", "move": "18"},
        {"pos": "63", "move": ""},
        {"pos": "64", "move": ""},
        {"pos": "65", "move": ""},
        {"pos": "66", "move": ""},
        {"pos": "67", "move": ""},
        {"pos": "68", "move": ""},
        {"pos": "69", "move": ""},
        {"pos": "70", "move": ""},
        {"pos": "71", "move": "92"},
        {"pos": "72", "move": ""},
        {"pos": "73", "move": ""},
        {"pos": "74", "move": ""},
        {"pos": "75", "move": ""},
        {"pos": "76", "move": ""},
        {"pos": "77", "move": ""},
        {"pos": "78", "move": ""},
        {"pos": "79", "move": ""},
        {"pos": "80", "move": "99"},
        {"pos": "81", "move": ""},
        {"pos": "82", "move": ""},
        {"pos": "83", "move": ""},
        {"pos": "84", "move": ""},
        {"pos": "85", "move": ""},
        {"pos": "86", "move": ""},
        {"pos": "87", "move": ""},
        {"pos": "88", "move": ""},
        {"pos": "89", "move": ""},
        {"pos": "90", "move": ""},
        {"pos": "91", "move": ""},
        {"pos": "92", "move": ""},
        {"pos": "93", "move": ""},
        {"pos": "94", "move": ""},
        {"pos": "95", "move": "56"},
        {"pos": "96", "move": ""},
        {"pos": "97", "move": "78"},
        {"pos": "98", "move": ""},
        {"pos": "99", "move": ""},
        {"pos": "100", "move": ""}
    ]
    DICE_MIN = 1
    DICE_MAX = 6

    def __init__(self, user_id: int, user_name: str,
                 player_num: int, player_pos: int = 0) -> None:
        """ Creates a player from the specified parameters. """
        self.id = user_id
        self.name = user_name
        self.num = player_num
        self.pos = player_pos

    def make_move(self) -> str:
        """ Performs a player's move. """
        dice_roll = random.randint(Player.DICE_MIN, Player.DICE_MAX)
        player_roll = f"{self.name} rolled a {dice_roll}.\n"
        rolled_pos = self.pos + dice_roll
        # Player landed on a position greater than 100.
        if rolled_pos > 100:
            return player_roll + f"{self.name} doesn't move."
        # Check for snake or ladder.
        new_pos = Player.BOARD[rolled_pos]['move']
        # Player did not land on a snake or ladder.
        if not new_pos:
            self.pos = rolled_pos
            return player_roll + f"{self.name} moved to {rolled_pos}."
        # Player landed on a snake.
        if int(new_pos) < rolled_pos:
            self.pos = int(new_pos)
            return player_roll + f"{self.name} slid down a snake at " \
                                 f"{rolled_pos} to {new_pos}!"
        # Player landed on a ladder.
        if int(new_pos) > rolled_pos:
            self.pos = int(new_pos)
            return player_roll + f"{self.name} climbed a ladder at " \
                                 f"{rolled_pos} to {new_pos}!"
