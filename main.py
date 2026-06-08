from Engine import Engine
from Game import Game
from Gapi import Gapi

if __name__ == "__main__":
    api = Gapi()
    game = Game()
    Engine(game, api, api).run()
