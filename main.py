from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer, AnalyticalDiscardPlayer, DNPRPlayer
from utils.game import Game
from utils.neural_nets import DiscardNetV1, DiscardTrainer, DiscardNetV2
from utils.simulator import Simulator


if __name__ == '__main__':

    net = DiscardNetV1()
    DiscardTrainer.train(
        net, lr = 1e-3, wd = 1e-4, epochs = 10, batch_size = 32, pool_size = 8, num_workers = 8
    )

    input('... preventing program from continuing by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    game = Game(
        player1 = RandomPlayer(),
        player2 = AnalyticalDiscardPlayer(),
        wait_after_move = None,
        wait_after_info = True,
        show_opponents_hand = False,
        visuals = True,
        measure_statistics = True
    )

    game.play()

    input('... preventing program from continuing by waiting for input ...')
