from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer
from utils.game import Game

from utils.helpers import Scoring

if __name__ == '__main__':
    input('... waiting for input ...')

    game = Game(UserPlayer(),
                RandomPlayer(),
                wait_after_move = 500,
                show_opponents_hand = False)

    game.play()
