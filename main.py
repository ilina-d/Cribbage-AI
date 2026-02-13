from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer, DiscardProPlayer
from utils.game import Game


if __name__ == '__main__':
    input('... preventing program from continuing by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    game = Game(DiscardProPlayer(),
                UserPlayer(),
                wait_after_move = 150,
                wait_after_info = False,
                show_opponents_hand = False)

    game.play()
