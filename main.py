from Engine import Engine
from Game import Game
from Gapi import Gapi

if __name__ == "__main__":
    api = Gapi()  # pygame wrapper
    game = Game()  # game logic
    Engine(game, api.renderer, api.input).run()  # start loop
