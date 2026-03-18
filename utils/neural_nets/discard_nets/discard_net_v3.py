from torch import nn

from .base_discard_net import BaseDiscardNet


class DiscardNetV3(BaseDiscardNet):
    """
    Neural network for discarding cards.

    ------

    Network structure:

    INPUT
    -> Linear(512), Tanh
    -> Linear(256), Tanh
    -> Linear(128), Tanh
    OUTPUT
    """

    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 512),
            nn.Tanh(),
            nn.Linear(512, 256),
            nn.Tanh(),
            nn.Linear(256, 128),
            nn.Tanh(),
            nn.Linear(128, self.OUTPUT_SIZE)
        )
        self.net.to(self.device)


__all__ = ['DiscardNetV3']
