import random
import time

from utils.assets import Display
from utils.players import BasePlayer, UserPlayer
from utils.helpers import CardDeck
from utils.helpers import Scoring


class Game:
    """ Cribbage game logic and flow. """

    state: dict[str, ...] = None
    card_deck: CardDeck = None
    dealers_crib: list[str] = None
    called_go: bool = False


    def __init__(self, player1: BasePlayer, player2: BasePlayer, visuals: bool = True,
                 wait_after_move: int | str | None = 'input') -> None:
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

        def wait_func():
            if wait_after_move is None:
                return
            if wait_after_move == 'input':
                input('... waiting for input ...')
                return
            time.sleep(wait_after_move / 1000)
        self.wait_after_move = wait_func

        self.reset_game()


    def reset_game(self) -> None:
        """ Reset the game state to its starting form and clear all player data. """

        self.state = {
            'cribs' : [[], [], []],
            'current_crib_idx' : 0,
            'crib_sums': [0, 0, 0],
            'starter_card': None,
            'dealer' : random.choice([self.player1, self.player2]),
            'player1' : self.player1,
            'player2' : self.player2
        }

        self.dealers_crib = []

        self.card_deck = CardDeck(shuffle = True)
        self.player1.cards = []
        self.player2.cards = []

        self.called_go = False


    def prepare_new_round(self) -> None:
        """ Prepare the game state for a new round. """

        self.state['cribs'] = [[], [], []]
        self.state['current_crib_idx'] = 0
        self.state['crib_sums'] = [0, 0, 0]
        self.state['starter_card'] = None
        self.state['dealer'] = self.player1 if self.state['dealer'] == self.player2 else self.player2
        self.dealers_crib = []

        self.card_deck = CardDeck(shuffle = True)
        self.player1.cards = self.card_deck.deal_cards(6)
        self.player2.cards = self.card_deck.deal_cards(6)

        self.called_go = False


    def check_win(self) -> BasePlayer | None:
        """
        Check if there is a winner in the current game state.

        ------

        Returns:
            The winning player or None if there is no winner yet.
        """

        if self.player1.points >= 121:
            return self.player1

        if self.player2.points >= 121:
            return self.player2

        return None


    def discard_cards(self, player: BasePlayer) -> None:
        """
        Update the game state based on the player's move during the Discard phase.

        ------

        Arguments:
            player: The player whose turn it is to play.
        """

        discarded_cards = player.discard_cards(self.state)
        self.dealers_crib.extend(discarded_cards)


    def play_card(self, player: BasePlayer) -> None:
        """
        Update the game state based on the player's move during the Play phase.

        ------

        Arguments:
            player: The player whose turn it is to play.
        """

        played_card = player.play_card(self.state)

        if played_card == "GO":
            if self.called_go:
                self.state['current_crib_idx'] += 1
                self.called_go = False
            else:
                self.called_go = True
                Scoring.score_go(self.state, player, update_points = True)
            return

        current_crib_idx = self.state['current_crib_idx']
        self.state['cribs'][current_crib_idx].append(played_card)
        Scoring.score_card(self.state, player, update_points = True)

        self.state['crib_sums'][current_crib_idx] += CardDeck.get_card_worth(played_card)
        if self.state['crib_sums'][current_crib_idx] == 31:
            self.state['current_crib_idx'] += 1
            self.called_go = False


    def play(self) -> None:
        """ Start the main game loop. """

        self.reset_game()
        winner = None

        while winner is None:
            self.prepare_new_round()
            dealer = self.state['dealer']
            non_dealer = self.player1 if dealer == self.player2 else self.player2

            # DISCARD PHASE
            self.discard_cards(self.player1)
            if not isinstance(self.player1, UserPlayer):
                self.wait_after_move()

            self.discard_cards(self.player2)
            self.wait_after_move()

            self.state.starter_card = self.card_deck.deal_cards(1)[0]

            Scoring.score_heels(self.state, update_points = True)

            # PRE-CALCULATION FOR THE SHOW PHASE
            hand_score_dealer = Scoring.score_hand(self.state, dealer, update_points = False)
            hand_score_non_dealer = Scoring.score_hand(self.state, non_dealer, update_points = False)

            # PLAY PHASE
            current_player = non_dealer

            while self.player1.cards or self.player2.cards:
                prev_called_go = self.called_go
                self.play_card(current_player)

                if not isinstance(current_player, UserPlayer):
                    self.wait_after_move()

                winner = self.check_win()
                if winner:
                    break

                if not (self.called_go and self.called_go == prev_called_go):
                    current_player = self.player1 if current_player == self.player2 else self.player2

            # SHOW PHASE
            non_dealer.points += hand_score_non_dealer
            self.wait_after_move()

            winner = self.check_win()
            if winner:
                break

            dealer += hand_score_dealer
            self.wait_after_move()

            winner = self.check_win()
            if winner:
                break

            Scoring.score_crib(self.state, self.dealers_crib, update_points = True)
            self.wait_after_move()

            winner = self.check_win()
            if winner:
                break

        # GAME END


__all__ = ['Game']
