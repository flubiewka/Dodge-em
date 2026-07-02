from Game import Game
from Interfaces import IInputProvider, IRenderer


class Engine:
    def __init__(self, game: Game, renderer: IRenderer, input_provider: IInputProvider):
        self._game = game
        self._renderer = renderer
        self._input_provider = input_provider

    def run(self) -> None:
        self._renderer.setup(self._game)
        dt = 0.0

        while True:
            match self._input_provider.poll_events():
                case "quit":
                    break
                case "reset":
                    self._game.reset()

            actions1, actions2 = self._input_provider.get_actions()
            self._game.update(dt, actions1, actions2)
            self._renderer.render(self._game)
            dt = self._renderer.tick()
