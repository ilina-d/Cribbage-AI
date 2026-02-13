import random

from .base_player import BasePlayer
from utils.helpers.discard_evaluator import DiscardEvaluator

class DiscardProPlayer(BasePlayer):
    """ Player agent that makes random moves. """

    def discard_cards(self, state: dict[str, ...]) -> list[str]:

        cards = DiscardEvaluator.get_discard_stats(self.cards, state['dealer'] == self)
        cards = cards['recommended']['cards']

        self.cards.remove(cards[0])
        self.cards.remove(cards[1])

        return cards


    def play_card(self, state: dict[str, ...]) -> str:

        card = random.choice(self.get_valid_moves(state))

        if card != "GO":
            self.cards.remove(card)

        return card


__all__ = ['DiscardProPlayer']
