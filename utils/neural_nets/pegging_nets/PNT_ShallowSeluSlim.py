from torch import nn

from .base_pegging_net import BasePeggingNet


class PNT_ShallowSeluSlim(BasePeggingNet):
    """ Neural network for playing cards. """

    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(self.INPUT_SIZE, 512),
            nn.SELU(),
            nn.Linear(512, 256),
            nn.SELU(),
            nn.Linear(256, 128),
            nn.SELU(),
            nn.Linear(128, self.OUTPUT_SIZE)
        )

        for layer in self.net:
            if isinstance(layer, nn.Linear):
                nn.init.kaiming_normal_(layer.weight, mode = 'fan_in', nonlinearity = 'linear')
                nn.init.zeros_(layer.bias)

        self.net.to(self.device)


__all__ = ['PNT_ShallowSeluSlim']
