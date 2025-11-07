import random

from .base_player import BasePlayer

class RandomPlayer(BasePlayer):
    """ Player agent that makes random moves. """

    def discard_cards(self, state: dict[str, ...]) -> list[str]:

        cards = random.sample(self.cards, 2)

        self.cards.remove(cards[0])
        self.cards.remove(cards[1])

        return cards


    def play_card(self, state: dict[str, ...]) -> str:

        card = random.choice(self.get_valid_moves(state))

        if card != "GO":
            self.cards.remove(card)

        return card