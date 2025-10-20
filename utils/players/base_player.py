from abc import abstractmethod, ABC

from utils.helpers import State


class BasePlayer(ABC):
    """ Abstract representation of a player. """

    def __init__(self):
        self.cards = []


    @abstractmethod
    def discard_cards(self, state: State) -> list[str, str]:
        pass


    @abstractmethod
    def play_card(self, state: State) -> str:
        pass


__all__ = ['BasePlayer']
