import random

from utils.assets import Display
from utils.players import BasePlayer


class Game:
    """ Cribbage game logic and flow. """

    def __init__(self, player1: BasePlayer, player2: BasePlayer, visuals: bool = True,
                 wait_after_move: int | str | None = 'input',) -> None:
        """
        Create and initialize an instance of the Game class.

        ------

        Note on Players:
            If one of the players is a UserPlayer object, player1 and player2 are
            assigned such that player1 is always the UserPlayer. Only one of the
            players can be controlled by a user.

        ------

        Waiting Methods:
            - int | Number of seconds to wait.
            - "input" | Wait until input is given.
            - None | No waiting.

        ------

        Arguments:
            player1: The first player object.
            player2: The second player object.
            visuals: Whether to display the game flow in the terminal.
            wait_after_move: The method for waiting after each move.
        """

        # TODO: Continue here...


"""
GAME CONTENTS:
- Shuffle
- Crib
- The entire state
- Who's the dealer?
    - Maybe let the player (if user_player) to pick a card to choose the first dealer
    - or just add the illusion of choice and do random.choice() anyway :troll_face:
- Players (objects, so it can call player.make_move() ):
    - Player 1 is always the one shown below (usually the user)
- Reset/Create new or starting state:
    - With option to reset completely
    - Or to start a new turn (points remain, dealer changes, ...)
- Dealing
- Option to toggle printing/display
- wait after move?


STATE REPRESENTATION:
- Played cards (in the middle):
    - Separated into cribs of max sum 31
- Extra card (on the side)
- Who's crib it is
- Current points for both players
- Amount of cards left for each player?
- 
"""


__all__ = ['Game']
