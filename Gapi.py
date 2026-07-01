import math

import pygame

from Interfaces import IInputProvider, IRenderer


class PyGameInput(IInputProvider):
    def __copy__(self):
        raise TypeError("PyGameInput does not support copying")

    def __deepcopy__(self, _):
        raise TypeError("PyGameInput does not support copying")

    def poll_events(self) -> str:
        # check quit/reset keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_r:
                    return "reset"
        return "continue"

    def get_actions(self):
        # read keyboard state
        k = pygame.key.get_pressed()
        a1 = {
            "forward": k[pygame.K_w],
            "brake": k[pygame.K_s],
            "left": k[pygame.K_a],
            "right": k[pygame.K_d],
            "nitro": k[pygame.K_LSHIFT],
        }
        a2 = {
            "forward": k[pygame.K_UP],
            "brake": k[pygame.K_DOWN],
            "left": k[pygame.K_LEFT],
            "right": k[pygame.K_RIGHT],
            "nitro": k[pygame.K_RETURN] or k[pygame.K_KP_ENTER],
        }
        return a1, a2


class PyGameRenderer(IRenderer):
    WIDTH, HEIGHT = 960, 540
    FPS = 60
    CAR_COLORS = ((255, 214, 0), (0, 200, 80))

    def __copy__(self):
        raise TypeError("PyGameRenderer does not support copying")

    def __deepcopy__(self, _):
        raise TypeError("PyGameRenderer does not support copying")

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dodge 'em")
        self._clock = pygame.time.Clock()
        self._camera = pygame.Vector2()
        self._track_surf = None
        self._track_offset = (0, 0)
        self._dashes = []
        self._font = pygame.font.SysFont(None, 26)
        self._font_big = pygame.font.SysFont(None, 36)
        self._car_imgs = [self._make_car(c) for c in self.CAR_COLORS]

    def _make_car(self, color):
        # draw car sprite
        s = pygame.Surface((48, 28), pygame.SRCALPHA)
        pygame.draw.rect(s, color, s.get_rect(), border_radius=6)  # car
        pygame.draw.rect(s, (25, 25, 25), s.get_rect(), 2, border_radius=6)  # window
        pygame.draw.rect(s, (255, 255, 255), pygame.Rect(28, 6, 10, 16))  # border
        return s

    def setup(self, game):
        # build track + wall checker
        self._track_surf, self._track_offset = self._build_track()
        ox, oy = self._track_offset
        surf = self._track_surf

        def is_wall(x, y):
            lx, ly = int(x - ox), int(y - oy)
            if not (0 <= lx < surf.get_width() and 0 <= ly < surf.get_height()):
                return True
            try:
                return surf.get_at((lx, ly))[3] == 0
            except IndexError:
                return False

        game.set_wall_checker(is_wall)

    def render(self, game):
        # center camera on cars
        cx = (game.p1.car.pos.x + game.p2.car.pos.x) / 2
        cy = (game.p1.car.pos.y + game.p2.car.pos.y) / 2
        self._camera.x = cx - self.WIDTH / 2
        self._camera.y = cy - self.HEIGHT / 2

        self._screen.fill((18, 18, 24))
        ox, oy = self._track_offset
        if self._track_surf:
            self._screen.blit(
                self._track_surf, (ox - self._camera.x, oy - self._camera.y)
            )

        # dashed centerline
        for a, b in self._dashes:
            pygame.draw.line(
                self._screen,
                (255, 255, 255),
                (a[0] - self._camera.x, a[1] - self._camera.y),
                (b[0] - self._camera.x, b[1] - self._camera.y),
                3,
            )

        # finish line stripes
        fy, fx0, fx1 = game.FINISH_Y, game.FINISH_X0, game.FINISH_X1
        for i in range(10):
            x = fx0 + (fx1 - fx0) * i / 10
            xn = fx0 + (fx1 - fx0) * (i + 1) / 10
            c = (255, 255, 255) if i % 2 == 0 else (20, 20, 20)
            pygame.draw.line(
                self._screen,
                c,
                (x - self._camera.x, fy - self._camera.y),
                (xn - self._camera.x, fy - self._camera.y),
                10,
            )

        # draw cars
        for ps, img in zip((game.p1, game.p2), self._car_imgs):
            rot = pygame.transform.rotate(img, -ps.car.angle)
            r = rot.get_rect(
                center=(ps.car.pos.x - self._camera.x, ps.car.pos.y - self._camera.y)
            )
            self._screen.blit(rot, r)

        # HUD panels
        for x, label, laps, color in (
            (14, "P1 WASD", game.p1.laps, (255, 214, 0)),
            (self.WIDTH - 164, "P2 Arrows", game.p2.laps, (0, 200, 80)),
        ):
            s = pygame.Surface((150, 60), pygame.SRCALPHA)
            pygame.draw.rect(s, (20, 20, 30, 200), s.get_rect(), border_radius=8)
            pygame.draw.rect(s, (*color, 180), s.get_rect(), 2, border_radius=8)
            s.blit(self._font.render(label, True, color), (8, 6))
            s.blit(
                self._font_big.render(f"Laps: {laps}", True, (230, 230, 230)), (8, 28)
            )
            self._screen.blit(s, (x, 14))

        pygame.display.flip()

    def tick(self):
        # cap framerate, return dt
        return self._clock.tick(self.FPS) / 1000

    def _build_track(self):
        # generate oval track surface
        cx, cy, rx, ry, road_w = 800, 600, 600, 300, 300
        pad = road_w // 2 + 20
        pts = [
            (
                cx + int(rx * math.cos(math.radians(i))),
                cy + int(ry * math.sin(math.radians(i))),
            )
            for i in range(0, 360, 5)
        ]
        min_x = min(p[0] for p in pts) - pad
        min_y = min(p[1] for p in pts) - pad
        surf = pygame.Surface(
            (
                max(p[0] for p in pts) + pad - min_x,
                max(p[1] for p in pts) + pad - min_y,
            ),
            pygame.SRCALPHA,
        )
        loc = [(p[0] - min_x, p[1] - min_y) for p in pts]
        for p in loc:
            pygame.draw.circle(surf, (200, 200, 200), p, (road_w + 40) // 2)
        pygame.draw.lines(surf, (200, 200, 200), True, loc, road_w + 40)
        for p in loc:
            pygame.draw.circle(surf, (80, 80, 80), p, road_w // 2)
        pygame.draw.lines(surf, (80, 80, 80), True, loc, road_w)
        self._dashes = [
            (pts[i], pts[(i + 1) % len(pts)]) for i in range(0, len(pts), 4)
        ]
        return surf, (min_x, min_y)


class Gapi:
    # holds renderer and input provider

    def __init__(self):
        self.renderer = PyGameRenderer()
        self.input = PyGameInput()
