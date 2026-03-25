from utils.assets import Display
from utils.game import Game
from utils.simulator import Simulator
from utils.helpers import DiscardEvaluator, Scoring

from utils.players import *
from utils.neural_nets import *

from utils.neural_nets.discard_nets.DNT_DeepLeakySlim import DNT_DeepLeakySlim
from utils.neural_nets.discard_nets.DNT_DeepReluSlim import DNT_DeepReluSlim
from utils.neural_nets.discard_nets.DNT_DeepSeluSlim import DNT_DeepSeluSlim
from utils.neural_nets.discard_nets.DNT_DeepSigmoidSlim import DNT_DeepSigmoidSlim
from utils.neural_nets.discard_nets.DNT_DeepTanhSlim import DNT_DeepTanhSlim

from utils.neural_nets.discard_nets.DNT_DeepLeakyWide import DNT_DeepLeakyWide
from utils.neural_nets.discard_nets.DNT_DeepReluWide import DNT_DeepReluWide
from utils.neural_nets.discard_nets.DNT_DeepSeluWide import DNT_DeepSeluWide
from utils.neural_nets.discard_nets.DNT_DeepSigmoidWide import DNT_DeepSigmoidWide
from utils.neural_nets.discard_nets.DNT_DeepTanhWide import DNT_DeepTanhWide

from utils.neural_nets.discard_nets.DNT_ShallowLeakySlim import DNT_ShallowLeakySlim
from utils.neural_nets.discard_nets.DNT_ShallowReluSlim import DNT_ShallowReluSlim
from utils.neural_nets.discard_nets.DNT_ShallowSeluSlim import DNT_ShallowSeluSlim
from utils.neural_nets.discard_nets.DNT_ShallowSigmoidSlim import DNT_ShallowSigmoidSlim
from utils.neural_nets.discard_nets.DNT_ShallowTanhSlim import DNT_ShallowTanhSlim

from utils.neural_nets.discard_nets.DNT_ShallowLeakyWide import DNT_ShallowLeakyWide
from utils.neural_nets.discard_nets.DNT_ShallowReluWide import DNT_ShallowReluWide
from utils.neural_nets.discard_nets.DNT_ShallowSeluWide import DNT_ShallowSeluWide
from utils.neural_nets.discard_nets.DNT_ShallowSigmoidWide import DNT_ShallowSigmoidWide
from utils.neural_nets.discard_nets.DNT_ShallowTanhWide import DNT_ShallowTanhWide

from utils.neural_nets.trainers.seeded_discard_trainer import SeededDiscardTrainer

import torch
import numpy


if __name__ == '__main__':

    NETS = [
        DNT_DeepLeakySlim, DNT_DeepReluSlim, DNT_DeepSeluSlim, DNT_DeepSigmoidSlim, DNT_DeepTanhSlim,
        DNT_DeepLeakyWide, DNT_DeepReluWide, DNT_DeepSeluWide, DNT_DeepSigmoidWide, DNT_DeepTanhWide,
        DNT_ShallowLeakySlim, DNT_ShallowReluSlim, DNT_ShallowSeluSlim, DNT_ShallowSigmoidSlim, DNT_ShallowTanhSlim,
        DNT_ShallowLeakyWide, DNT_ShallowReluWide, DNT_ShallowSeluWide, DNT_ShallowSigmoidWide, DNT_ShallowTanhWide,
    ]

    STATIC_PARAMS = {
        'lr' : 0.0001, 'wd' : 0.01, 'epochs': 1000, 'batch_size': 10, 'pool_size': 0,
        'alpha': 1, 'alpha_step': 10, 'alpha_decay': 0.02, 'accumulate_loss' : False
    }

    PARAMS_VALUES = [
        {'inflate_advantage' : False, 'info' : 'NormAdv'},
        {'inflate_advantage' : True, 'info' : 'InfAdv'},
    ]

    SEEDS = [11, 13, 17, 19, 23, 29, 31, 37]

    encoder = 'SimpleEncoderNormalized'
    seed = 37
    SeededDiscardTrainer.load_state_pool(seed)
    for net_cls in NETS:
        for params in PARAMS_VALUES:
            numpy.random.seed(seed)
            torch.manual_seed(seed)
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False

            name = f'{encoder}_{net_cls.__name__}_{params["info"]}_seed{seed}'
            net = net_cls()

            params = params.copy()
            params.pop('info')
            args = STATIC_PARAMS.copy()
            args.update(params)

            SeededDiscardTrainer.train(discard_network = net, **args)
            SeededDiscardTrainer.save(discard_network = net, file_name = name, comment = '/')

    input('... preventing program from continuing by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    game = Game(
        player1 = UserPlayer(),
        player2 = DAPGPlayer(),
        first_dealer = None,
        wait_after_move = 200,
        wait_after_info = True,
        show_opponents_hand = False,
        visuals = True,
        measure_statistics = False
    )

    game.play()

    input('... preventing program from continuing by waiting for input ...')
