from utils.assets import Display
from utils.players import RandomPlayer, UserPlayer
from utils.game import Game

if __name__ == '__main__':

    game = Game(UserPlayer(), RandomPlayer())

    game.play()