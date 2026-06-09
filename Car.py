import math


class MathVector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def length(self):
        return math.hypot(self.x, self.y)

    def scale_to_length(self, target_length):
        l = self.length()
        if l > 0:
            self.x = (self.x / l) * target_length
            self.y = (self.y / l) * target_length

    def lerp(self, other, t):
        return MathVector2(
            self.x + (other.x - self.x) * t, self.y + (other.y - self.y) * t
        )

    def __add__(self, other):
        return MathVector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return MathVector2(self.x - other.x, self.y - other.y)

    def __mul__(self, s):
        return MathVector2(self.x * s, self.y * s)

    def __rmul__(self, s):
        return self.__mul__(s)


class Car:
    ACCELERATION = 900.0
    TURN_SPEED = 180.0
    DRAG = 4.0
    MAX_SPEED = 320.0
    SIZE = (48, 28)

    def __init__(self, x: float, y: float):
        self.pos = MathVector2(x, y)
        self.vel = MathVector2()
        self.angle = -90.0

    def __copy__(self):
        raise TypeError("Car does not support copying")

    def __deepcopy__(self, _):
        raise TypeError("Car does not support copying")

    def reset(self, x: float, y: float):
        self.pos = MathVector2(x, y)
        self.vel = MathVector2()
        self.angle = -90.0

    def update(self, dt: float, actions: dict):
        rad = math.radians(self.angle)
        forward = MathVector2(math.cos(rad), math.sin(rad))
        speed = self.vel.length()

        turn = 0
        if actions["left"]:
            turn -= 1 if speed >= 10 else speed / 10
        if actions["right"]:
            turn += 1 if speed >= 10 else speed / 10
        self.angle += turn * self.TURN_SPEED * dt

        thrust, max_speed = 0.0, self.MAX_SPEED
        if actions["forward"]:
            thrust += 1.0
        if actions["brake"]:
            thrust -= 0.5
        if actions["nitro"]:
            thrust += 2.5
            max_speed *= 2

        if thrust:
            self.vel += forward * (self.ACCELERATION * thrust * dt)
        if speed > max_speed:
            self.vel.scale_to_length(max_speed)
        if speed > 0:
            self.vel = self.vel.lerp(MathVector2(), min(self.DRAG * dt, 1.0) * 0.5)

        self.pos += self.vel * dt
