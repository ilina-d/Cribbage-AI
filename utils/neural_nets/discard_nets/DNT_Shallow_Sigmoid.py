from torch import nn

from .base_discard_net import BaseDiscardNet


class DNT_Shallow_Sigmoid(BaseDiscardNet):
    """ Neural network for discarding cards. """

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 1024),
            nn.Sigmoid(),
            nn.Linear(1024, 512),
            nn.Sigmoid(),
            nn.Linear(512, 256),
            nn.Sigmoid(),
            nn.Linear(256, self.OUTPUT_SIZE),
        )
        self.net.to(self.device)


__all__ = ['DNT_Shallow_Sigmoid']
