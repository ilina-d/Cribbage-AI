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

    sim = Simulator(
        player1 = RandomPlayer(),
        player2 = RandomPlayer(),
        num_simulations = 10000,
        num_workers = 999,
        measure_performance = True
    )

    sim.start()

    input('... preventing program from continuing by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    game = Game(
        player1 = UserPlayer(),
        player2 = RandomPlayer(),
        first_dealer = 'player2',
        wait_after_move = 'input',
        wait_after_info = True,
        show_opponents_hand = False,
        visuals = True,
        measure_statistics = True
    )

    game.play()

    input('... preventing program from continuing by waiting for input ...')
