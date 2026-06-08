from Engine import Engine
from Game import Game
from Gapi import Gapi

# from gweb import Gweb  ← swap here to change renderer, nothing else changes

if __name__ == "__main__":
    renderer = Gapi()
    game = Game()
    Engine(game, renderer).run()
