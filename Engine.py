class Engine:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.running = True

    def run(self):
        dt = 0
        while self.running:
            match self.get_input():
                case "quit":
                    self.running = False
                case "reset":
                    self.game.reset()

            self.update(dt)
            self.render()

            dt = self.renderer.frame_end()

    def update(self, dt):
        self.game.update(dt)

    def render(self):
        self.renderer.render(self.game)

    def get_input(self):
        # Получить результат от рендера
        return self.renderer.poll_events()
