from utils.assets import Display
from utils.game import Game
from utils.simulator import Simulator
from utils.helpers import DiscardEvaluator, Scoring, StateEncoder

from utils.players import *
from utils.neural_nets import *


if __name__ == '__main__':

    input('... preventing program from starting by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    game = Game(
        player1 = DAPGPlayer(),
        player2 = DAPGPlayer(),
        first_dealer = None,
        wait_after_move = 500,
        wait_after_info = False,
        show_opponents_hand = False,
        visuals = True,
        measure_statistics = False
    )

    game.play()

    input('... preventing program from continuing by waiting for input ...')
