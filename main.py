from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer, AnalyticalDiscardPlayer, DNPRPlayer
from utils.game import Game
from utils.neural_nets import DiscardNetV1, DiscardTrainer, DiscardNetV2
from utils.simulator import Simulator


if __name__ == '__main__':
    nets_v1 = [
        'DNV1_48K_Independent', 'DNV1_48K_Supervised_aggressive',
        'DNV1_48K_Supervised_recommended1', 'DNV1_48K_Supervised_recommended2'
    ]

    nets_v2 = [
        'DNV2_48K_Independent', 'DNV2_48K_Supervised_aggressive',
        'DNV2_48K_Supervised_recommended1', 'DNV2_48K_Supervised_recommended2'
    ]

    for net_name in nets_v1:
        net = DiscardNetV1()
        net.load_weights(net_name)

        sim = Simulator(
            player1 = DNPRPlayer(discard_net = net),
            player2 = RandomPlayer(),
            num_simulations = 1000,
            measure_performance = False
        )

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
