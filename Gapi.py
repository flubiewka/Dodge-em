import math

import pygame

from Interfaces import IInputProvider, IRenderer


class Gapi(IRenderer, IInputProvider):
    WIDTH, HEIGHT = 960, 540
    FPS = 60

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dodge 'em")
        self.clock = pygame.time.Clock()

        self._camera = pygame.Vector2()
        self._track_surf: pygame.Surface | None = None
        self._track_offset = (0, 0)
        self._font = pygame.font.SysFont(None, 26)
        self._car_image = self._build_car_image()

    def _build_car_image(self) -> pygame.Surface:
        w, h = 48, 28
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        rect = surf.get_rect()
        pygame.draw.rect(surf, (255, 214, 0), rect, border_radius=6)
        pygame.draw.rect(surf, (25, 25, 25), rect, 2, border_radius=6)
        pygame.draw.rect(
            surf, pygame.Rect(w * 0.58, h * 0.22, w * 0.2, h * 0.56), (255, 255, 255)
        )
        return surf

    def setup(self, game) -> None:
        self._track_surf, self._track_offset = self._build_track()

    def poll_events(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_r:
                    return "reset"
        return "continue"

    def get_actions(self) -> dict[str, bool]:
        keys = pygame.key.get_pressed()
        return {
            "forward": keys[pygame.K_w] or keys[pygame.K_UP],
            "brake": keys[pygame.K_s] or keys[pygame.K_DOWN],
            "left": keys[pygame.K_a] or keys[pygame.K_LEFT],
            "right": keys[pygame.K_d] or keys[pygame.K_RIGHT],
            "nitro": keys[pygame.K_LSHIFT],
        }

    def render(self, game) -> None:
        self._update_camera(game.player.pos)

        self.screen.fill((18, 18, 24))
        pygame.draw.rect(
            self.screen, (32, 32, 44), self.screen.get_rect(), 6, border_radius=18
        )

        ox, oy = self._track_offset
        self.screen.blit(self._track_surf, (ox - self._camera.x, oy - self._camera.y))

        self._draw_car(game.player)

        text = self._font.render(
            f"x={int(game.player.pos.x)}  "
            f"y={int(game.player.pos.y)}  "
            f"speed={game.player.vel.length():.1f}",
            True,
            (180, 180, 180),
        )
        self.screen.blit(text, (18, 14))

        pygame.display.flip()

    def _draw_car(self, player) -> None:
        rotated = pygame.transform.rotate(self._car_image, -player.angle)
        rect = rotated.get_rect(
            center=(player.pos.x - self._camera.x, player.pos.y - self._camera.y)
        )
        self.screen.blit(rotated, rect)

    def tick(self) -> float:
        return self.clock.tick(self.FPS) / 1000

    def _update_camera(self, target) -> None:
        self._camera.x = target.x - self.WIDTH / 2
        self._camera.y = target.y - self.HEIGHT / 2

    @staticmethod
    def _build_track() -> tuple[pygame.Surface, tuple]:
        points = [
            (
                800 + int(600 * math.cos(math.radians(i))),
                600 + int(300 * math.sin(math.radians(i))),
            )
            for i in range(0, 360, 5)
        ]
        road_w = 300
        pad = road_w // 2 + 20

        min_x = min(p[0] for p in points) - pad
        min_y = min(p[1] for p in points) - pad
        max_x = max(p[0] for p in points) + pad
        max_y = max(p[1] for p in points) + pad

        surf = pygame.Surface((max_x - min_x, max_y - min_y), pygame.SRCALPHA)
        local = [(p[0] - min_x, p[1] - min_y) for p in points]

        for p in local:
            pygame.draw.circle(surf, (200, 200, 200), p, (road_w + 40) // 2)
        pygame.draw.lines(surf, (200, 200, 200), True, local, road_w + 40)

        for p in local:
            pygame.draw.circle(surf, (80, 80, 80), p, road_w // 2)
        pygame.draw.lines(surf, (80, 80, 80), True, local, road_w)

        return surf, (min_x, min_y)
