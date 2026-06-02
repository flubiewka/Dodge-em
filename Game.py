from Car import Car
from Engine import Engine
from renderer_Gapi.Gapi import Gapi


class Game:
    def __init__(self):
        self.renderer = Gapi()
        self.engine = Engine(self, self.renderer)
        self.player = Car(960 / 2, 540 / 2)
        self.renderer.init_refs(self.player)

    def start(self):
        self.engine.run()

    def update(self, dt):
        actions = self.renderer.get_input_actions()
        bounds = self.renderer.get_bounds()
        self.player.update(dt, actions, bounds)

    def reset(self):
        start_position = (960 / 2, 540 / 2)
        self.player.reset(start_position)
