from torch import nn

from .base_pegging_net import BasePeggingNet


class PeggingNetV1(BasePeggingNet):
    """
        Neural network for playing cards.

        ------

        Network structure:

        INPUT
        -> Linear(256), LayerNorm(256), ReLU, Dropout(0.2)
        -> Linear(128), LayerNorm(128), ReLU, Dropout(0.2)
        -> Linear(64),  ReLU
        OUTPUT
        """

    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 256),
            nn.LayerNorm(256),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(256, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, self.OUTPUT_SIZE)
        )
        self.net.to(self.device)


__all__ = ["PeggingNetV1"]