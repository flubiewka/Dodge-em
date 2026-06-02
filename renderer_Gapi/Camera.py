import pygame


class Camera:
    def __init__(self, width, height):
        self.pos = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def update(self, target_pos):
        self.pos.x = target_pos.x - self.width / 2
        self.pos.y = target_pos.y - self.height / 2
