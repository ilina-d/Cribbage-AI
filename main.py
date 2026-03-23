from utils.assets import Display
from utils.game import Game
from utils.simulator import Simulator
from utils.helpers import DiscardEvaluator, Scoring

from utils.players import *
from utils.neural_nets import *


if __name__ == '__main__':

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
