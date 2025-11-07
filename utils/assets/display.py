from sty import fg as Text, bg as Back, rs as Rest
from os import system as sys_call

from utils.helpers import CardDeck
from utils.players import BasePlayer, UserPlayer


class Display:
    """ Visualizing the game flow in the terminal. """

    WIDTH: int = 99
    HEIGHT: int = 33

    PADDING: int = 3

    CARD_WIDTH: int = 7
    CARD_HEIGHT: int = 5

    DEALER_TOP: tuple[int, int] = (PADDING, PADDING)
    DEALER_BOTTOM: tuple[int, int] = (HEIGHT - PADDING - CARD_HEIGHT, PADDING)

    HAND_TOP: tuple[int, int] = (PADDING, DEALER_TOP[1] + CARD_WIDTH * 2)
    HAND_BOTTOM: tuple[int, int] = (HEIGHT - PADDING - CARD_HEIGHT, DEALER_BOTTOM[1] + CARD_WIDTH * 2)

    STARTER_CARD: tuple[int, int] = (HEIGHT // 2 - 2, PADDING)

    POINTS_TOP: tuple[int, int] = (CARD_HEIGHT, WIDTH - PADDING - 7)
    POINTS_BOTTOM: tuple[int, int] = (HEIGHT - CARD_HEIGHT - 1, WIDTH - PADDING - 7)

    PLAY_CARD_TOP: tuple[int, int] = (HAND_TOP[0] + 2 * CARD_HEIGHT, HAND_TOP[1])
    PLAY_CARD_BOTTOM: tuple[int, int] = (HAND_BOTTOM[0] - 2 * CARD_HEIGHT, HAND_BOTTOM[1])

    current_card_pos: list[int] = list(PLAY_CARD_TOP)


    def __init__(self, player1: BasePlayer, player2: BasePlayer, show_opponents_hand: bool = False) -> None:
        """
        Create and initialize an instance of the Display class.

        ------

        Note on show_opponents_hand:
            If neither player is controlled by a user, this argument is preset to True.

        ------

        Arguments:
            player1: The first player object.
            player2: The second player object.
            show_opponents_hand: Whether to reveal the opponents hand.
        """

        self.matrix = [[]]

        self.player1 = player1
        self.player2 = player2

        self.show_opponents_hand = show_opponents_hand
        if not isinstance(player1, UserPlayer):
            self.show_opponents_hand = True

        sys_call("")  # Run a system call to enable colors in the terminal.


    def clear(self, clear_matrix: bool = False) -> None:
        """
        Clear the display.

        ------

        Arguments:
            clear_matrix: Whether to clear the display matrix or just the terminal display.
        """

        if clear_matrix:
            self.matrix = [[f'{Back.da_green} {Back.rs}' for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
            self.current_card_pos = list(self.PLAY_CARD_TOP)

        print('\033[H', end='')


    def print(self, tricks_info: list[str] = None, show_board: bool = False) -> None:
        """
        Print the display to the terminal.

        ------

        Arguments:
            tricks_info: Scoring information to print below the board.
            show_board: Whether to print the board or not.
        """

        if show_board:
            lines = [''.join(line) + '\n' for line in self.matrix]
            print(''.join(lines), flush=True)

        if tricks_info is None:
            return

        for trick in tricks_info:
            print(trick + ' ' * (60 - len(trick)))

        for _ in range(10 - len(tricks_info)):
            print(' ' * 60)


    def update_starter(self, state: dict[str, ...]) -> None:
        """
        Update the terminal display after the starter card is altered.

        ------

        Arguments:
             state: The current state of the game.
        """

        card = state['starter_card']
        card_matrix = self.get_card_matrix(card) if card else self.get_flipped_card_matrix()

        card_row, card_col = self.STARTER_CARD

        for row in range(card_row, card_row + self.CARD_HEIGHT):
            for col in range(card_col, card_col + self.CARD_WIDTH):
                self.matrix[row][col] = card_matrix[row - card_row][col - card_col]


    def update_crib(self, state: dict[str, ...]) -> None:
        """
        Update the terminal display after the dealer's crib is altered.

        ------

        Arguments:
             state: The current state of the game.
        """

        card_matrix = self.get_flipped_card_matrix()

        card_row, card_col = self.DEALER_TOP if state['dealer'] == state['player2'] else self.DEALER_BOTTOM

        for row in range(card_row, card_row + self.CARD_HEIGHT):
            for col in range(card_col, card_col + self.CARD_WIDTH):
                self.matrix[row][col] = card_matrix[row - card_row][col - card_col]


    def update_play(self, state: dict[str, ...], player: BasePlayer, option: str) -> None:
        """
        Update the terminal display after player makes a move.

        ------

        Options:
            - "stay" | Playable area remains unchanged. Used when the player can't add to the crib.
            - "next_card" | Draws the last played card and moves over one space. Used when a card is played.
            - "next_crib_31" | Draws the last played card and moves to next crib. Used when the player scores 31.
            - "next_crib_go" | Moves to the next crib. Used when neither player can add to the crib.

        ------

        Arguments:
            state: The current state of the game.
            player: The player who made the move.
            option: The update option.
        """

        if option == "stay":
            return

        card_col = self.current_card_pos[1]
        card_row = self.PLAY_CARD_TOP[0] if player == state["player2"] else self.PLAY_CARD_BOTTOM[0]

        if option in ("next_card", "next_crib_31"):
            if option == 'next_crib_31':
                card_matrix = self.get_card_matrix(state['cribs'][state['current_crib_idx'] - 1][-1])
            else:
                card_matrix = self.get_card_matrix(state["cribs"][state["current_crib_idx"]][-1])

            for row in range(card_row, card_row + self.CARD_HEIGHT):
                for col in range(card_col, card_col + self.CARD_WIDTH):
                    self.matrix[row][col] = card_matrix[row - card_row][col - card_col]

            self.update_hand(state, player)

        self.current_card_pos[1] = card_col + 1 + self.CARD_WIDTH

        if option == "next_crib_31":
            self.current_card_pos[1] += 1 + self.CARD_WIDTH


    def update_hand(self, state: dict[str, ...], player: BasePlayer) -> None:
        """
        Update the terminal display after the player's hand is altered.

        ------

        Arguments:
            state: The current state of the game.
            player: The player whose hand is altered.
        """

        player_cards = player.cards + [None] * (6 - len(player.cards))
        if not self.show_opponents_hand and player == state["player2"]:
            player_cards = ["F"] * len(player.cards) + [None] * (6 - len(player.cards))

        card_row, card_col = self.HAND_TOP if player == state["player2"] else self.HAND_BOTTOM

        for card in player_cards:

            if card is None:
                card_matrix = self.get_blank_card_matrix()
            elif card == "F":
                card_matrix = self.get_flipped_card_matrix()
            else:
                card_matrix = self.get_card_matrix(card)

            for row in range(card_row, card_row + self.CARD_HEIGHT):
                for col in range(card_col, card_col + self.CARD_WIDTH):
                    self.matrix[row][col] = card_matrix[row - card_row][col - card_col]

            card_col += 1 + self.CARD_WIDTH


    def update_points(self, state: dict[str, ...], player: BasePlayer) -> None:
        """
        Update the terminal display after the player scores points.

        ------

        Arguments:
            state: The current state of the game.
            player: The player who scored points.
        """

        points = f'{player.points} pts'

        pts_row, pts_col = self.POINTS_TOP if player == state['player2'] else self.POINTS_BOTTOM

        for col in range(pts_col, pts_col + len(points)):
            self.matrix[pts_row][col] = f'{Back.da_green}{Text.li_yellow}{points[col - pts_col]}{Rest.all}'


    def get_card_matrix(self, card: str) -> list[list[str]]:
        """
        Convert a card from rank-suit format to printable format.

        ------

        Arguments:
            card: The card to convert.

        ------

        Returns:
            The same card in a format ready for printing.
        """

        rank = card[0]
        suit = CardDeck.get_card_suit(card)

        color = Text.red if card[1] in 'DH' else Text.black

        matrix = [[f'{Back.white} {Back.rs}' for _ in range(self.CARD_WIDTH)] for _ in range(self.CARD_HEIGHT)]

        matrix[2][3] = f'{Back.white}{color}{rank}{Rest.all}'
        matrix[0][1] = matrix[-1][-2] = f'{Back.white}{color}{suit}{Rest.all}'

        return matrix


    def get_flipped_card_matrix(self) -> list[list[str]]:
        """
        Get a flipped card in printable format.

        ------

        Returns:
            A flipped card in a format ready for printing.
        """

        return [[f'{Back.da_red}{Text.white}░{Rest.all}' for _ in range(self.CARD_WIDTH)]
                for _ in range(self.CARD_HEIGHT)]


    def get_blank_card_matrix(self) -> list[list[str]]:
        """
        Get a blank card in printable format.

        ------

        Returns:
             A blank card in a format ready for printing.
        """

        return [[f'{Back.da_green} {Back.rs}' for _ in range(self.CARD_WIDTH)] for _ in range(self.CARD_HEIGHT)]


__all__ = ['Display']
