from Car import Car


class Game:
    """Чистая игровая логика. Никакого I/O — только состояние и правила."""

    START_POS = (800, 600)

    def __init__(self):
        self.player = Car(*self.START_POS)

    def update(self, dt: float, actions: dict) -> None:
        self.player.update(dt, actions)

    def reset(self) -> None:
        self.player.reset(*self.START_POS)
