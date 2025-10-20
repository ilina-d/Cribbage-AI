import random
import time

from utils.assets import Display
from utils.players import BasePlayer, UserPlayer
from utils.helpers import CardDeck, State


class Game:
    """ Cribbage game logic and flow. """

    card_deck: CardDeck = None
    dealers_crib: list[str] = None
    state: State = None
    called_go: bool = False
    current_crib: int = 0

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
            - int | Number of milliseconds to wait.
            - "input" | Wait until input is given.
            - None | No waiting.

        ------

        Arguments:
            player1: The first player object.
            player2: The second player object.
            visuals: Whether to display the game flow in the terminal.
            wait_after_move: The method for waiting after each move.
        """

        self.player1, self.player2 = player1, player2
        if isinstance(player2, UserPlayer):
            if isinstance(player1, UserPlayer):
                raise Exception("Both players cannot be a UserPlayer instance.")
            self.player1, self.player2 = player2, player1

        self.visuals = visuals
        self.display = Display()

        def waiting(start_time: float = None):
            if wait_after_move is None:
                return
            if wait_after_move == 'input':
                input('... waiting for input ...')
                return
            if start_time:
                if time.time() - start_time <= wait_after_move:
                    time.sleep(int(wait_after_move - (time.time() - start_time)) / 1000)
                return
            else:
                time.sleep(wait_after_move / 1000)
        self.wait_after_move = waiting

        self.reset_game()


    def prepare_new_round(self):
        """ Prepare the game state for a new round. """

        if not self.state.dealer:
            self.state.dealer = random.choice([self.player1, self.player2])
        else:
            self.state.dealer = self.player1 if self.state.dealer == self.player2 else self.player2

        self.state.cribs = [[], [], []]
        self.state.starter_card = None
        self.dealers_crib = []

        self.card_deck = CardDeck(shuffle=True)
        self.player1.cards = self.card_deck.deal_cards(6)
        self.player2.cards = self.card_deck.deal_cards(6)

        self.called_go = False
        self.current_crib = 0


    def reset_game(self):
        """ Reset the game state to its starting form and clear all player data. """

        self.state = State()
        self.card_deck = CardDeck(shuffle=True)
        self.dealers_crib = []

        self.player1.cards = []
        self.player2.cards = []

        self.called_go = False
        self.current_crib = 0


    def discard_cards(self, player: BasePlayer) -> None:
        """
        Update the game state based on player's discarded cards.

        ------

        Arguments:
            player: The player whose turn it is to play.
        """

        discarded_cards = player.discard_cards(self.state)

        self.dealers_crib.extend(discarded_cards)


    def play_card(self, player: BasePlayer) -> None:
        """
        Update the game state based on player's played card.

        ------

        Arguments:
            player: The player whose turn it is to play.
        """

        played_card = player.play_card(self.state)

        if played_card == "GO":
            if self.called_go:
                self.current_crib += 1
                self.called_go = False
            else:
                self.called_go = True
                # score go for other player
            return

        self.state.cribs[self.current_crib].append(played_card)

        # score played card
        # if crib score of current_crib is 31, current_crib +=1 and set called_go to false!!!!!


    def score_hand(self, player: BasePlayer) -> int:
        """
        Score cards at the end of the round for the given player.

        ------

        Arguments:
            player: The player whose hand is being scored.

        ------

        Returns:
            The score of the players hand with the current starter card.
        """

        # score player
        pass


    def play(self) -> None:
        """ Start the main game loop. """

        self.reset_game()
        winner = None

        while winner is None:
            self.prepare_new_round()

            # discard phase
            self.discard_cards(self.player1)
            self.discard_cards(self.player2)

            self.state.starter_card = self.card_deck.deal_cards(1)[0]

            # calc hand score + starter card
            hand_score_dealer = self.score_hand(self.state.dealer)
            hand_score_non_dealer = \
                self.score_hand(self.player1) if self.player2 == self.state.dealer else self.score_hand(self.player2)

            # play phase
            current_player = self.player1 if self.state.dealer == self.player2 else self.player2

            while self.player1.cards or self.player2.cards:
                prev_called_go = self.called_go
                self.play_card(current_player)

                winner = self.state.check_win()
                if winner:
                    break

                if not (self.called_go and self.called_go == prev_called_go):
                    current_player = self.player1 if current_player == self.player2 else self.player2

            # show phase
            dealer_idx, non_dealer_idx = (0, 1) if self.player1 == self.state.dealer else (1, 0)

            self.state.points[non_dealer_idx] += hand_score_non_dealer
            winner = self.state.check_win()
            if winner:
                break

            self.state.points[dealer_idx] += hand_score_dealer
            winner = self.state.check_win()
            if winner:
                break

        # game end
        print('game end ')


__all__ = ['Game']
