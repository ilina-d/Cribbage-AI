from abc import abstractmethod, ABC


class BasePlayer(ABC):
    """ Abstract representation of a player. """

    def __init__(self):
        self.cards = []
        self.points = 0


    @abstractmethod
    def discard_cards(self, state: dict[str, ...]) -> list[str, str]:
        pass


    @abstractmethod
    def play_card(self, state: dict[str, ...]) -> str:
        pass


__all__ = ['BasePlayer']
