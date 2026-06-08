import math

import pygame


class Car:
    """Физика и внешний вид машины. Не знает про рендерер или ввод."""

    ACCELERATION = 900.0
    TURN_SPEED = 180.0
    DRAG = 4.0
    MAX_SPEED = 320.0
    SIZE = (48, 28)

    def __init__(self, x: float, y: float):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2()
        self.angle = -90.0
        self._image = self._build_image()

    def _build_image(self) -> pygame.Surface:
        w, h = self.SIZE
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        rect = surf.get_rect()
        pygame.draw.rect(surf, (255, 214, 0), rect, border_radius=6)
        pygame.draw.rect(surf, (25, 25, 25), rect, 2, border_radius=6)
        pygame.draw.rect(
            surf, (255, 255, 255), pygame.Rect(w * 0.58, h * 0.22, w * 0.2, h * 0.56)
        )
        return surf

    def reset(self, x: float, y: float) -> None:
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2()
        self.angle = -90.0

    def update(self, dt: float, actions: dict) -> None:
        rad = math.radians(self.angle)
        forward = pygame.Vector2(math.cos(rad), math.sin(rad))
        speed = self.vel.length()

        # Поворот
        turn = 0
        if actions["left"]:
            turn -= 1 if speed >= 10 else speed / 10
        if actions["right"]:
            turn += 1 if speed >= 10 else speed / 10
        self.angle += turn * self.TURN_SPEED * dt

        # Тяга
        thrust = 0.0
        max_speed = self.MAX_SPEED
        if actions["forward"]:
            thrust += 1.0
        if actions["brake"]:
            thrust -= 0.5
        if actions["nitro"]:
            thrust += 2.5
            max_speed = 1000.0

        if thrust:
            self.vel += forward * self.ACCELERATION * thrust * dt
        if speed > max_speed:
            self.vel.scale_to_length(max_speed)
        if speed > 0:
            self.vel = self.vel.lerp(pygame.Vector2(), min(self.DRAG * dt, 1.0) * 0.5)

        self.pos += self.vel * dt

    def draw(self, surface: pygame.Surface, camera: pygame.Vector2) -> None:
        rotated = pygame.transform.rotate(self._image, -self.angle)
        rect = rotated.get_rect(center=(self.pos.x - camera.x, self.pos.y - camera.y))
        surface.blit(rotated, rect)
