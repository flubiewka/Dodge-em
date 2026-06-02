import pygame

from Renderer import Renderer
from renderer_Gapi.Camera import Camera
from renderer_Gapi.InputHandler import InputHandler
from renderer_Gapi.TrackRenderer import TrackRenderer
from renderer_Gapi.UIManager import UIManager


class Gapi(Renderer):
    def __init__(self):
        SCREEN_WIDTH = 960
        SCREEN_HEIGHT = 540

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.display.set_caption("Dodge 'em")

        self.track = TrackRenderer()

        self.Input = None
        self.Ui = None
        self.running = True
        self.dt = 0.0

    def init_refs(self, player):
        self.Input = InputHandler()
        self.Ui = UIManager(player, self.screen)

    def poll_events(self):
        if self.Input:
            return self.Input.analyse()
        return True

    def frame_end(self):
        pygame.display.flip()
        self.dt = self.clock.tick(60) / 1000
        return self.dt

    def render(self, game):
        self.camera.update(game.player.position)
        self.screen.fill((18, 18, 24))

        #
        pygame.draw.rect(
            self.screen, (32, 32, 44), self.screen.get_rect(), 6, border_radius=18
        )

        if not self.track.is_track_rendered:
            self.track.render_static_track()

        draw_x = self.track.track_offset[0] - self.camera.pos.x
        draw_y = self.track.track_offset[1] - self.camera.pos.y
        self.screen.blit(self.track.track_surface, (draw_x, draw_y))

        game.player.draw(self.screen, self.camera.pos)

        if self.Ui:
            self.Ui.render()

    def get_bounds(self):
        return {"width": 960, "height": 540}

    def get_input_actions(self):
        if self.Input:
            return self.Input.get_abstract_input()
        return {
            "forward": False,
            "brake": False,
            "left": False,
            "right": False,
            "nitro": False,
        }

    def is_car_on_track(self, player):
        if not self.track.is_track_rendered or self.track.track_surface is None:
            return None

        local_x = int(player.position.x - self.track.track_offset[0])
        local_y = int(player.position.y - self.track.track_offset[1])

        surf = self.track.track_surface

        if 0 <= local_x < surf.get_width() and 0 <= local_y < surf.get_height():
            color = surf.get_at((local_x, local_y))
            if (color.r, color.g, color.b) == (80, 80, 80):
                return "GRASS"

        return "OUT"
