from torch import nn

from utils.neural_nets.pegging_nets.base_pegging_net import BasePeggingNet


class PeggingNetV2(BasePeggingNet):
    """
        Neural network for playing cards.

        ------

        Network structure:

        INPUT
        -> Linear(512), ReLU
        -> Linear(256), ReLU
        -> Linear(128), ReLU
        OUTPUT
        """

    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, self.OUTPUT_SIZE)
        )
        self.net.to(self.device)


__all__ = ["PeggingNetV2"]
