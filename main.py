from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer, AnalyticalDiscardPlayer, DNPRPlayer, DAPNPlayer
from utils.game import Game
from utils.neural_nets import DiscardNetV1, DiscardTrainer, DiscardNetV2, \
    PeggingTrainer, PeggingNetV1
from utils.simulator import Simulator


if __name__ == '__main__':

    pegging_net = PeggingNetV1()
    PeggingTrainer.train(pegging_net, 1e-4, 1e-3, 1_000, opponent = RandomPlayer(),
                         batch_size = 100, pool_size = 20, early_stop = False, num_workers = 20)

    PeggingTrainer.save(pegging_net, "PNV1_1K_VSRandom", comment="Small test batch", logs = True)

    input('... test ...')

    pegging_net = PeggingNetV1()
    pegging_net.load_weights(file_name = "PNV1_1K_VSRandom")

    sim = Simulator(DAPNPlayer(pegging_net, play_style ='aggressive'),
                    AnalyticalDiscardPlayer(play_style = 'aggressive'),
                    100)
    sim.start()

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
