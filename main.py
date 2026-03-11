from utils.assets import Display
from utils.game import Game
from utils.simulator import Simulator

from utils.players import RandomPlayer, UserPlayer, DAPNPlayer, DAPRPlayer, DNPRPlayer
from utils.neural_nets import DiscardTrainer, PeggingTrainer, \
    DiscardNetV1, DiscardNetV2, DiscardNetV3, PeggingNetV1, PeggingNetV2


if __name__ == '__main__':

    net = PeggingNetV2()
    PeggingTrainer.train(
        pegging_network = net,
        lr = 1e-4,
        wd = 1e-3,
        epochs = 10_000,
        opponent = RandomPlayer(),
        batch_size = 100,
        pool_size = 20,
        num_workers = 24,
        early_stop = False
    )

    PeggingTrainer.save(
        pegging_network = net,
        file_name = 'PNV2_1M_RandomOpponent',
        comment = 'PeggingNetV2 plays 1M games against RandomPlayer.'
    )

    net = DiscardNetV3()
    DiscardTrainer.train(
        discard_network = net,
        lr = 1e-4,
        wd = 1e-3,
        epochs = 10_000,
        batch_size = 100,
        pool_size = 20,
        num_workers = 24,
        play_style = 'recommended',
        alpha = 1,
        alpha_step = 100,
        alpha_decay = 0.02,
        early_stop = False
    )

    DiscardTrainer.save(
        discard_network = net,
        file_name = 'DNV3_1M_Supervised_recommended',
        comment = 'DiscardNetV3 plays 1M games with "recommended" play-style and coaching. '
                  'Starting with alpha=1 and lowering it by 0.02 every 100 epochs, '
                  'reaching alpha=0 at the 5000th epoch.'
    )

    input('... preventing program from continuing by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    pegging_net = PeggingNetV1()
    pegging_net.load_weights(file_name = "PNV1_1K_VSRandom")

    game = Game(
        player1 = RandomPlayer(),
        player2 = RandomPlayer(),
        wait_after_move = 500,
        wait_after_info = True,
        show_opponents_hand = False,
        visuals = True,
        measure_statistics = True
    )

    game.play()

    input('... preventing program from continuing by waiting for input ...')
