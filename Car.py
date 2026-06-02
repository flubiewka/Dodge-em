import math

import pygame


class Car:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2()
        self.angle = -90.0
        self.acceleration = 900.0
        self.turn_speed = 180.0
        self.drag = 4.0
        self.max_speed = 320.0
        self.size = pygame.Vector2(48, 28)

        self.base_image = pygame.Surface(
            (int(self.size.x), int(self.size.y)), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.base_image, (255, 214, 0), self.base_image.get_rect(), border_radius=6
        )
        pygame.draw.rect(
            self.base_image,
            (25, 25, 25),
            self.base_image.get_rect(),
            2,
            border_radius=6,
        )
        pygame.draw.rect(
            self.base_image,
            (255, 255, 255),
            pygame.Rect(
                self.size.x * 0.58,
                self.size.y * 0.22,
                self.size.x * 0.2,
                self.size.y * 0.56,
            ),
        )

    def reset(self, position):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2()
        self.angle = -90.0

    def update(self, dt, actions, bounds):
        angle_radians = math.radians(self.angle)
        forward = pygame.Vector2(math.cos(angle_radians), math.sin(angle_radians))

        turn = 0
        speed = self.velocity.length()

        if actions["left"]:
            if speed < 10:
                turn -= speed / 10
            else:
                turn -= 1
        if actions["right"]:
            if speed < 10:
                turn += speed / 10
            else:
                turn += 1

        self.angle += turn * self.turn_speed * dt

        thrust = 0.0
        if actions["forward"]:
            thrust += 1.0
        if actions["brake"]:
            thrust -= 0.5

        if actions["nitro"]:
            thrust += 2.5
            self.max_speed = 1000

        if thrust != 0.0:
            self.velocity += forward * self.acceleration * thrust * dt

        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        if speed > 0:
            self.velocity = self.velocity.lerp(
                pygame.Vector2(), min(self.drag * dt, 1.0) * 0.5
            )

        self.position += self.velocity * dt

        # half_w = self.size.x / 2
        # half_h = self.size.y / 2
        # if self.position.x < half_w:
        #     self.position.x = half_w
        #     self.velocity.x *= -0.25
        # elif self.position.x > bounds["width"] - half_w:
        #     self.position.x = bounds["width"] - half_w
        #     self.velocity.x *= -0.25

        # if self.position.y < half_h:
        #     self.position.y = half_h
        #     self.velocity.y *= -0.25
        # elif self.position.y > bounds["height"] - half_h:
        #     self.position.y = bounds["height"] - half_h
        #     self.velocity.y *= -0.25

    def draw(self, surface, camera_pos=(0, 0)):
        rotated = pygame.transform.rotate(self.base_image, -self.angle)
        draw_x = self.position.x - camera_pos[0]
        draw_y = self.position.y - camera_pos[1]
        rect = rotated.get_rect(center=(draw_x, draw_y))
        surface.blit(rotated, rect)
