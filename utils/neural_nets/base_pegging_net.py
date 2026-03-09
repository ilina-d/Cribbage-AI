import torch
from torch import nn
from torch.nn import functional as F

from utils.helpers import StateEncoder, CardDeck


class BasePeggingNet(nn.Module):
    """ Base neural network for training pegging policies. """

    INPUT_SIZE = 208
    OUTPUT_SIZE = 5
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def __init__(self) -> None:
        """ Create a new BasePeggingNet instance. """

        super().__init__()

        self.net = None


    def load_weights(self, file_name: str) -> None:
        """
        Load the weights from a pretrained network (at trained_nets/pegging_nets/file_name.pt).

        ------

        Arguments:
            file_name: The file name to load from.
        """

        self.net.load_state_dict(torch.load(f'trained_nets/discard_nets/{file_name}.pt', map_location = self.device))


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """ Send an input though the net and get an output. """

        return self.net(x)


    def get_distribution_policy(self, player_score: int, opponent_score: int, is_dealer: bool,
                                current_crib_sum: int, current_crib_cards: list[str], starter_card: str,
                                player_hand: list[str]) -> list[tuple[str, torch.Tensor]]:
        """
        Get the processed output of the network for a given input.

        ------

        Arguments:
            player_score: The neural network player's score.
            opponent_score: The opponent's score.
            is_dealer: Whether the neural network player is the dealer.
            current_crib_sum: The total of the current crib.
            current_crib_cards: The played cards in the current crib.
            starter_card: The starter card.
            player_hand: The neural network player's cards in hand.

        ------

        Returns:
            A list of all 5 possible actions (4 cards and 'GO') along with their log-softmax values.
        """

        encoded_state = StateEncoder.encode_state_for_pegging_phase(
            player_score, opponent_score, is_dealer, current_crib_sum, current_crib_cards, starter_card, player_hand
        )

        outputs = self.net(torch.tensor(encoded_state, dtype=torch.float32, device=self.device))

        invalid_mask = [i < len(player_hand) and CardDeck.get_card_worth(player_hand[i]) + current_crib_sum <= 31
                        for i in range(4)]
        if True in invalid_mask:
            invalid_mask.append(False)
        else:
            invalid_mask.append(True)

        outputs[~torch.tensor(invalid_mask)] = float('-inf')
        probs = F.log_softmax(outputs, dim=-1)

        actions = []
        for card, prob in zip(player_hand + ['GO'], probs):
            actions.append((card, prob))

        return actions


    def get_pegging_action(self, player_score: int, opponent_score: int, is_dealer: bool,
                           current_crib_sum: int, current_crib_cards: list[str], starter_card: str,
                           player_hand: list[str]) -> tuple[str, torch.Tensor]:
        """
        Choose which card to play based on the given state.

        ------

        Arguments:
            player_score: The neural network player's score.
            opponent_score: The opponent's score.
            is_dealer: Whether the neural network player is the dealer.
            current_crib_sum: The total of the current crib.
            current_crib_cards: The played cards in the current crib.
            starter_card: The starter card.
            player_hand: The neural network player's cards in hand.

        ------

        Returns:
            The card chosen to be played along with its confidence score.
        """

        distribution = self.get_distribution_policy(player_score, opponent_score, is_dealer, current_crib_sum,
                                                    current_crib_cards, starter_card, player_hand)
        best_card = max(distribution, key = lambda x: x[1].item())
        return best_card[0], best_card[1]


__all__ = ["BasePeggingNet"]