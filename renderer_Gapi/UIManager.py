import pygame


class UIManager:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.font = pygame.font.SysFont(None, 26)

    def render(self):
        position_text = self.font.render(
            f"x={int(self.player.position.x)}  y={int(self.player.position.y)}  speed={self.player.velocity.length():.1f}",
            True,
            (180, 180, 180),
        )
        self.screen.blit(position_text, (18, 14))
