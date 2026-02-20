import torch
from torch import nn
from torch.nn import functional as F

from utils.helpers import StateEncoder

class BaseDiscardNet(nn.Module):
    """ Base neural network for training discard policies. """

    INPUT_SIZE = 105
    OUTPUT_SIZE = 6
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def __init__(self) -> None:
        """ Create a new BaseDiscardNet instance. """

        super().__init__()

        self.net = None


    def load_weights(self, file_name: str) -> None:
        """
        Load the weights from a pretrained network (at trained_nets/discard_nets/file_name.pt).

        ------

        Arguments:
            file_name: The file name to load from.
        """

        self.net.load_state_dict(torch.load(f'trained_nets/discard_nets/{file_name}.pt', map_location = self.device))


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """ Send an input though the net and get an output. """

        return self.net(x)


    def get_discard_action(self, player_score: int, opponent_score: int, is_dealer: bool,
                           player_hand: list[str]) -> tuple[str, str, torch.Tensor, torch.Tensor]: # :3
        """
        Choose which cards to discard based on the given state.

        ------

        Arguments:
            player_score: The neural network player's score.
            opponent_score: The opponent's score.
            is_dealer: Whether the neural network player is the dealer.
            player_hand: The neural network player's cards in hand.

        ------

        Returns:
            The cards chosen to be discarded and their confidence scores.
        """

        encoded_state = StateEncoder.encode_state_for_discard_phase(player_score, opponent_score,
                                                                    is_dealer, player_hand)

        state_tensor = torch.tensor(encoded_state, dtype = torch.float32, device = self.device)

        outputs = self.net(state_tensor)
        probs = F.log_softmax(outputs, dim=-1)

        top2 = torch.topk(probs, k=2)
        idx1, idx2 = int(top2.indices[0]), int(top2.indices[1])

        return player_hand[idx1], player_hand[idx2], top2.values[0], top2.values[1]


__all__ = ['BaseDiscardNet']
