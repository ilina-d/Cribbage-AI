from torch import nn

from .base_discard_net import BaseDiscardNet


class DNT_ShallowSeluWide(BaseDiscardNet):
    """ Neural network for discarding cards. """

    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 1024),
            nn.SELU(),
            nn.Linear(1024, 512),
            nn.SELU(),
            nn.Linear(512, 256),
            nn.SELU(),
            nn.Linear(256, self.OUTPUT_SIZE),
            nn.Sigmoid()
        )

        for layer in self.net:
            if isinstance(layer, nn.Linear):
                nn.init.kaiming_normal_(layer.weight, mode = 'fan_in', nonlinearity = 'linear')
                nn.init.zeros_(layer.bias)

        self.net.to(self.device)


__all__ = ['DNT_ShallowSeluWide']
