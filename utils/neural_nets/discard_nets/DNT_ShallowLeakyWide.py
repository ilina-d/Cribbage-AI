from torch import nn

from .base_discard_net import BaseDiscardNet


class DNT_ShallowLeakyWide(BaseDiscardNet):
    """ Neural network for discarding cards. """

    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 1024),
            nn.LeakyReLU(),
            nn.Linear(1024, 512),
            nn.LeakyReLU(),
            nn.Linear(512, 256),
            nn.LeakyReLU(),
            nn.Linear(256, self.OUTPUT_SIZE)
        )

        self.net.to(self.device)


__all__ = ['DNT_ShallowLeakyWide']
