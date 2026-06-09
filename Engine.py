from Game import Game
from Interfaces import IInputProvider, IRenderer


class Engine:
    def __init__(self, game: Game, renderer: IRenderer, input_provider: IInputProvider):
        self.game = game
        self.renderer = renderer
        self.input_provider = input_provider

    def run(self) -> None:
        self.renderer.setup(self.game)
        dt = 0.0

        while True:
            match self.input_provider.poll_events():
                case "quit":
                    break
                case "reset":
                    self.game.reset()

            actions1, actions2 = self.input_provider.get_actions()
            self.game.update(dt, actions1, actions2)
            self.renderer.render(self.game)
            dt = self.renderer.tick()
