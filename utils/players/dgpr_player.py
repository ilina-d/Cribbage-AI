import random
import itertools
import copy

from .base_player import BasePlayer
from utils.helpers import Scoring, CardDeck

class DGPRPlayer(BasePlayer):
    """
    Player agent that plays greedy during the discard phase,
    but makes random moves during the pegging phase.
    """

    def discard_cards(self, state: dict[str, ...]) -> list[str]:

        state = copy.deepcopy(state)
        for starter_card in ['JH', 'JS', 'JC', 'JD']:
            if starter_card in self.cards:
                continue
            state['starter_card'] = starter_card
            break

        if state['starter_card'] is None:
            deck = CardDeck(shuffle = True)
            for starter_card in deck.cards:
                if starter_card in self.cards:
                    continue
                state['starter_card'] = starter_card
                break

        player_hand = self.cards.copy()

        best_combo = None
        best_score = float('-inf')

        for combo in itertools.combinations(player_hand, 2):
            self.cards = [card for card in player_hand if card not in combo]
            score, _ = Scoring.score_hand(state, self, update_points = False)

            if score > best_score:
                best_score = score
                best_combo = list(combo)

        self.cards = player_hand
        self.cards.remove(best_combo[0])
        self.cards.remove(best_combo[1])

        return best_combo


    def play_card(self, state: dict[str, ...]) -> str:

        card = random.choice(self.get_valid_moves(state))

        if card != "GO":
            self.cards.remove(card)

        return card


__all__ = ['DGPRPlayer']
