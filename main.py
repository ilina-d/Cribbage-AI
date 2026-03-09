from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer, AnalyticalDiscardPlayer, DNPRPlayer
from utils.game import Game
from utils.neural_nets import DiscardNetV1, DiscardTrainer, DiscardNetV2, PeggingTrainer, PeggingNetV1
from utils.simulator import Simulator


if __name__ == '__main__':

    pegging_net = PeggingNetV1()

    PeggingTrainer.train(
        pegging_net,
        lr = 1e-5,
        wd = 1e-6,
        epochs = 10_000,
        opponent = RandomPlayer(),
        batch_size = 100,
        pool_size = 20,
        num_workers = 24,
        early_stop = False,
    )

    PeggingTrainer.save(pegging_net, 'PNV1_0K_RandomOpponent', 'PeggingNetV1 plays 1M games against a random opponent.')

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
