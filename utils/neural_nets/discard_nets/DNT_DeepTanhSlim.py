from torch import nn

from .base_discard_net import BaseDiscardNet


class DNT_DeepTanhSlim(BaseDiscardNet):
    """ Neural network for discarding cards. """

    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 512),
            nn.Tanh(),
            nn.Linear(512, 512),
            nn.Tanh(),

            nn.Linear(512, 256),
            nn.Tanh(),
            nn.Linear(256, 256),
            nn.Tanh(),

            nn.Linear(256, 128),
            nn.Tanh(),
            nn.Linear(128, 128),
            nn.Tanh(),

            nn.Linear(128, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),

            nn.Linear(64, self.OUTPUT_SIZE)
        )
        self.net.to(self.device)


__all__ = ['DNT_DeepTanhSlim']
