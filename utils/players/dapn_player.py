from utils.players import BasePlayer
from utils.neural_nets import BasePeggingNet
from utils.helpers import DiscardEvaluator


class DAPNPlayer(BasePlayer):
    """
    Player agent that plays analytically during the discard phase and
    uses a neural network during the pegging phase.
    """

    def __init__(self, pegging_net: BasePeggingNet, play_style: str = 'recommended') -> None:
        """
        Create a new DAPNPlayer instance.

        ------

        Arguments:
            pegging_net: A pretrained pegging network.
        """
        super().__init__()
        self.pegging_net = pegging_net
        self.pegging_net.net.eval()
        self.play_style = play_style


    def discard_cards(self, state: dict[str, ...]) -> list[str]:

        stats = DiscardEvaluator.get_discard_stats(self.cards, state['dealer'] == self)
        cards = stats[self.play_style][0][0]

        self.cards.remove(cards[0])
        self.cards.remove(cards[1])

        return cards


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


__all__ = ['DAPNPlayer']
