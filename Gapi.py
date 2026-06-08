import math

import pygame


class Gapi:
    """
    Pygame-реализация Renderer.
    Весь pygame-код живёт здесь и только здесь.
    Camera, InputHandler, TrackRenderer, UIManager — приватные детали этого класса.
    """

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
        self._player = None

    # ── Renderer interface ─────────────────────────────────────────────────

    def setup(self, game) -> None:
        self._player = game.player
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

    def get_actions(self) -> dict:
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

        # Трасса
        ox, oy = self._track_offset
        self.screen.blit(self._track_surf, (ox - self._camera.x, oy - self._camera.y))

        # Машина
        game.player.draw(self.screen, self._camera)

        # HUD
        text = self._font.render(
            f"x={int(game.player.pos.x)}  "
            f"y={int(game.player.pos.y)}  "
            f"speed={game.player.vel.length():.1f}",
            True,
            (180, 180, 180),
        )
        self.screen.blit(text, (18, 14))

        pygame.display.flip()

    def tick(self) -> float:
        return self.clock.tick(self.FPS) / 1000

    # ── Private helpers ────────────────────────────────────────────────────

    def _update_camera(self, target: pygame.Vector2) -> None:
        self._camera.x = target.x - self.WIDTH / 2
        self._camera.y = target.y - self.HEIGHT / 2

    @staticmethod
    def _build_track() -> tuple[pygame.Surface, tuple]:
        """Строит поверхность трассы один раз при старте."""
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

        # Обочина
        for p in local:
            pygame.draw.circle(surf, (200, 200, 200), p, (road_w + 40) // 2)
        pygame.draw.lines(surf, (200, 200, 200), True, local, road_w + 40)

        # Дорога
        for p in local:
            pygame.draw.circle(surf, (80, 80, 80), p, road_w // 2)
        pygame.draw.lines(surf, (80, 80, 80), True, local, road_w)

        return surf, (min_x, min_y)
