import pygame


class InputHandler:
    def get_abstract_input(self):
        keys = pygame.key.get_pressed()
        return {
            "forward": keys[pygame.K_w] or keys[pygame.K_UP],
            "brake": keys[pygame.K_s] or keys[pygame.K_DOWN],
            "left": keys[pygame.K_a] or keys[pygame.K_LEFT],
            "right": keys[pygame.K_d] or keys[pygame.K_RIGHT],
            "nitro": keys[pygame.K_LSHIFT],
        }

    def analyse(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return "reset"
        return "continue"
