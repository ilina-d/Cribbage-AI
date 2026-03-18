from torch import nn

from .base_discard_net import BaseDiscardNet


class DiscardNetV4(BaseDiscardNet):
    """
    Neural network for discarding cards.

    ------

    Network structure:

    INPUT
    -> Linear(256), LeakyReLU(0.1), Dropout(0.2)
    -> Linear(256), LeakyReLU(0.1), Dropout(0.2)
    -> Linear(128), LeakyReLU(0.1), Dropout(0.2)
    -> Linear(64), LeakyReLU(0.1)
    OUTPUT
    """

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 256),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.2),

            nn.Linear(256, 256),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.2),

            nn.Linear(256, 128),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.2),

            nn.Linear(128, 64),
            nn.LeakyReLU(0.1),

            nn.Linear(64, self.OUTPUT_SIZE)
        )
        self.net.to(self.device)


__all__ = ['DiscardNetV4']
