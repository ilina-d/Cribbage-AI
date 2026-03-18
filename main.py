from utils.assets import Display
from utils.game import Game
from utils.simulator import Simulator
from utils.helpers import DiscardEvaluator, Scoring

from utils.players import *
from utils.neural_nets import *

from utils.neural_nets.discard_nets.DNT_Deep_Leaky import DNT_Deep_Leaky
from utils.neural_nets.discard_nets.DNT_Deep_Relu import DNT_Deep_Relu
from utils.neural_nets.discard_nets.DNT_Deep_Selu import DNT_Deep_Selu
from utils.neural_nets.discard_nets.DNT_Deep_Sigmoid import DNT_Deep_Sigmoid
from utils.neural_nets.discard_nets.DNT_Deep_Tanh import DNT_Deep_Tanh

from utils.neural_nets.discard_nets.DNT_Shallow_Leaky import DNT_Shallow_Leaky
from utils.neural_nets.discard_nets.DNT_Shallow_Relu import DNT_Shallow_Relu
from utils.neural_nets.discard_nets.DNT_Shallow_Selu import DNT_Shallow_Selu
from utils.neural_nets.discard_nets.DNT_Shallow_Sigmoid import DNT_Shallow_Sigmoid
from utils.neural_nets.discard_nets.DNT_Shallow_Tanh import DNT_Shallow_Tanh

from utils.neural_nets.trainers.DTT_StepAfterBackward import DTT_StepAfterBackward
from utils.neural_nets.trainers.DTT_StepAfterBackwardCubed import DTT_StepAfterBackwardCubed
from utils.neural_nets.trainers.DTT_ZeroBackwardStep import DTT_ZeroBackwardStep
from utils.neural_nets.trainers.DTT_ZeroBackwardStepCubed import DTT_ZeroBackwardStepCubed
from utils.neural_nets.trainers.DTT_ZeroStepBackward import DTT_ZeroStepBackward
from utils.neural_nets.trainers.DTT_ZeroStepBackwardCubed import DTT_ZeroStepBackwardCubed


if __name__ == '__main__':

    trainer_args = {
        'lr': 0.001,
        'wd': 0.000001,
        'epochs': 10_000,
        'batch_size': 10,
        'pool_size': 3,
        'early_stop': False,
        'play_style': 'recommended',
        'alpha': 1,
        'alpha_step': 10,
        'alpha_decay': 0.002,
    }

    trainers = [
        DTT_StepAfterBackward, DTT_StepAfterBackwardCubed,
        DTT_ZeroBackwardStep, DTT_ZeroBackwardStepCubed,
        DTT_ZeroStepBackward, DTT_ZeroStepBackwardCubed
    ]

    networks_deep = [DNT_Deep_Leaky, DNT_Deep_Relu, DNT_Deep_Selu, DNT_Deep_Sigmoid, DNT_Deep_Tanh]
    networks_shallow = [DNT_Shallow_Leaky, DNT_Shallow_Relu, DNT_Shallow_Selu, DNT_Shallow_Sigmoid, DNT_Shallow_Tanh]

    for network in networks_deep:
        for trainer in trainers:

            net = network()
            net_name = net.__class__.__name__
            trainer_name = trainer.__name__

            trainer.train(discard_network = net, **trainer_args)
            trainer.save(
                net,
                file_name = f'TEST_{net_name}__{trainer_name}',
                comment = f'{net_name} trained for 100K games with {trainer_name}'
            )

    input('... preventing program from continuing by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    game = Game(
        player1 = UserPlayer(),
        player2 = RandomPlayer(),
        wait_after_move = 'input',
        wait_after_info = True,
        show_opponents_hand = False,
        visuals = True,
        measure_statistics = True
    )

    game.play()

    input('... preventing program from continuing by waiting for input ...')
