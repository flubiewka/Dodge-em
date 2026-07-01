from typing import Callable

from Car import Car


class PlayerState:
    # car + lap counter
    def __init__(self, x: float, y: float):
        self._start = (x, y)
        self.car = Car(x, y)
        self.laps = 0
        self._away = True  # was outside finish zone

    def __copy__(self):
        raise TypeError("PlayerState does not support copying")

    def __deepcopy__(self, _):
        raise TypeError("PlayerState does not support copying")

    def check_lap(self, is_finish: Callable[[float, float], bool]):
        # detect crossing finish line
        near = is_finish(self.car.pos.x, self.car.pos.y)
        if near and self._away and self.car.vel.length() > 10:
            self.laps += 1
        self._away = not near

    def reset(self):
        # back to start position
        self.car.reset(*self._start)
        self.laps = 0
        self._away = True


class Game:
    FINISH_Y = 600
    FINISH_X0, FINISH_X1 = 1250, 1550

    def __init__(self):
        self.p1 = PlayerState(1350, 570)
        self.p2 = PlayerState(1450, 570)
        self._is_wall: Callable[[float, float], bool] = lambda x, y: (
            False
        )  # default: no walls

    def __copy__(self):
        raise TypeError("Game does not support copying")

    def __deepcopy__(self, _):
        raise TypeError("Game does not support copying")

    def set_wall_checker(self, fn: Callable[[float, float], bool]):
        # inject collision check
        self._is_wall = fn

    def _is_finish(self, x: float, y: float) -> bool:
        # inside finish rectangle
        return abs(y - self.FINISH_Y) < 30 and self.FINISH_X0 <= x <= self.FINISH_X1

    def update(self, dt: float, a1: dict, a2: dict):
        # advance both players
        for ps, actions in ((self.p1, a1), (self.p2, a2)):
            ps.car.update(dt, actions)
            self._check_wall(ps.car)
            ps.check_lap(self._is_finish)

    def _check_wall(self, car):
        # bounce off wall
        if self._is_wall(car.pos.x, car.pos.y):
            car.pos -= car.vel * 0.016
            car.vel = car.vel * -0.5

    def reset(self):
        # reset both players
        self.p1.reset()
        self.p2.reset()
