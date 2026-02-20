from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer, AnalyticalDiscardPlayer, DNPRPlayer
from utils.game import Game

from utils.neural_nets import DiscardNetV1, DiscardTrainer


net = DiscardNetV1()
DiscardTrainer.train(net, play_style = 'recommended', lr = 1e-3, wd = 1e-4, epochs = 30, early_stop = False)


if __name__ == '__main__':
    input('... preventing program from continuing by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    game = Game(RandomPlayer(),
                AnalyticalDiscardPlayer(),
                wait_after_move = 'input',
                wait_after_info = False,
                show_opponents_hand = False)

    game.play()
