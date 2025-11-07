from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer
from utils.game import Game

from utils.helpers import Scoring


if __name__ == '__main__':
    input('... waiting for input ...')

    game = Game(RandomPlayer(),
                UserPlayer(),
                wait_after_move = None,
                show_opponents_hand = False)

    game.play()
