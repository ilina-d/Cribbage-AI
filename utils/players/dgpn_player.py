import itertools
import copy

from utils.players import BasePlayer
from utils.neural_nets import BasePeggingNet
from utils.helpers import Scoring, CardDeck


class DGPNPlayer(BasePlayer):
    """
    Player agent that plays greedy during the discard phase
    and uses a neural network during the pegging phase.
    """

    def __init__(self, pegging_net: BasePeggingNet) -> None:
        """
        Create a new DAPNPlayer instance.

        ------

        Arguments:
            pegging_net: A pretrained pegging network.
        """
        super().__init__()
        self.pegging_net = pegging_net
        self.pegging_net.net.eval()


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

        opponent = state['player1'] if self == state['player2'] else state['player2']
        curr_crib_sum = state['crib_sums'][state['current_crib_idx']]
        curr_crib = state['cribs'][state['current_crib_idx']]

        card, _ = self.pegging_net.get_pegging_action(
            self.points, opponent.points, curr_crib_sum, curr_crib, self.cards
        )

        if card != 'GO':
            self.cards.remove(card)

        return card


__all__ = ['DGPNPlayer']
