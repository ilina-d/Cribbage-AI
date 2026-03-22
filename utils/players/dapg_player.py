import random
import copy

from .base_player import BasePlayer
from utils.helpers import DiscardEvaluator, Scoring


class DAPGPlayer(BasePlayer):
    """ Player agent that discards cards based on statistical analysis, but plays greedy during pegging. """

    def __init__(self, play_style: str = 'recommended') -> None:
        """
        Create a new DAPGPlayer instance.

        ------

        Arguments:
            play_style: The play style that will be used during discarding.
        """
        super().__init__()
        self.play_style = play_style


    def discard_cards(self, state: dict[str, ...]) -> list[str]:

        stats = DiscardEvaluator.get_discard_stats(self.cards, state['dealer'] == self)
        cards = stats[self.play_style][0][0]

        self.cards.remove(cards[0])
        self.cards.remove(cards[1])

        return cards


    def play_card(self, state: dict[str, ...]) -> str:

        moves = self.get_valid_moves(state)

        if moves == ['GO']:
            return 'GO'

        best_move = None
        best_score = float('-inf')

        for move in moves:
            new_state = copy.deepcopy(state)
            new_state['cribs'][new_state['current_crib_idx']].append(move)

            score, _ = Scoring.score_card(new_state, self, update_points=False)
            if score > best_score:
                best_score = score
                best_move = move

        self.cards.remove(best_move)

        return best_move


__all__ = ['DAPGPlayer']
