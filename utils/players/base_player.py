from abc import abstractmethod, ABC

from utils.helpers import CardDeck


class BasePlayer(ABC):
    """ Abstract representation of a player. """

    def __init__(self) -> None:
        """ Create a new player instance. """

        self.cards = []
        self.points = 0


    @abstractmethod
    def discard_cards(self, state: dict[str, ...]) -> list[str]:
        """
        Discard two cards from the hand to the dealer's crib.

        ------

        Arguments:
            state: The game state.

        ------

        Returns:
            The discarded cards.
        """

        pass


    @abstractmethod
    def play_card(self, state: dict[str, ...]) -> str:
        """
        Play a card from the hand onto the current crib.

        ------

        Arguments:
            state: The game state.

        -------

        Returns:
            The played card, or GO if a card cannot be played.
        """

        pass


    def get_valid_moves(self, state: dict[str, ...]) -> list[str]:
        """
        Get a list of valid moves for the given state.

        ------

        Arguments:
            state: The game state.

        ------

        Returns:
            A list of playable cards, or GO if there are none.
        """

        current_crib_sum = state['crib_sums'][state['current_crib_idx']]
        valid_cards = [card for card in self.cards if CardDeck.get_card_worth(card) + current_crib_sum <= 31]

        return valid_cards if valid_cards else ['GO']


__all__ = ['BasePlayer']
