from Game import Game
from Renderer import Renderer


class Engine:
    """Чистый игровой цикл. Не знает ни про pygame, ни про детали игры."""

    def __init__(self, game: Game, renderer: Renderer):
        self.game = game
        self.renderer = renderer

    def run(self) -> None:
        self.renderer.setup(self.game)
        dt = 0.0

        while True:
            match self.renderer.poll_events():
                case "quit":
                    break
                case "reset":
                    self.game.reset()

            actions = self.renderer.get_actions()
            self.game.update(dt, actions)
            self.renderer.render(self.game)
            dt = self.renderer.tick()
