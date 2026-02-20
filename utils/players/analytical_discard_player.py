import random

from .base_player import BasePlayer
from utils.helpers.discard_evaluator import DiscardEvaluator

class AnalyticalDiscardPlayer(BasePlayer):
    """ Player agent that discards cards based on statistical analysis, but plays randomly during pegging. """

    def discard_cards(self, state: dict[str, ...]) -> list[str]:

        stats = DiscardEvaluator.get_discard_stats(self.cards, state['dealer'] == self)
        cards = stats['recommended'][0][0]

        self.cards.remove(cards[0])
        self.cards.remove(cards[1])

        return cards


    def play_card(self, state: dict[str, ...]) -> str:

        card = random.choice(self.get_valid_moves(state))

        if card != "GO":
            self.cards.remove(card)

        return card


__all__ = ['AnalyticalDiscardPlayer']
