from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer, AnalyticalDiscardPlayer, DNPRPlayer
from utils.game import Game
from utils.neural_nets import DiscardNetV1, DiscardTrainer, DiscardNetV2, \
    PeggingTrainer, PeggingNetV1
from utils.simulator import Simulator


if __name__ == '__main__':

    pegging_net = PeggingNetV1()
    PeggingTrainer.train(pegging_net, 1e-3, 1e-4, 100, opponent = RandomPlayer(),
                         batch_size = 20, pool_size = 20, early_stop = False, num_workers = 20)

    input('... test ...')

    sim = Simulator(RandomPlayer(), RandomPlayer(), 1000)
    sim.start()

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
