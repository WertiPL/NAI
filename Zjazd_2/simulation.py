import pygame

MAP_MARGIN = 100


class Simulation:
    def __init__(self, game_map, train):
        """Initialize PyGame and all other resources."""
        self.map = game_map
        self.train = train

        pygame.init()
        self.screen = pygame.display.set_mode(
            size=[self.map.dimensions[0], self.map.dimensions[1] + MAP_MARGIN],
            flags=pygame.SCALED,
            vsync=1
        )

    def __del__(self):
        """On program end, cleanup resources."""
        pygame.quit()

    def run(self):
        """Main simulation loop that handles events and draws current data."""

        clock = pygame.time.Clock()

        while True:
            if not self.__handle_events():
                break

            time_delta = clock.tick()

            self.train.move(time_delta)

            self.__draw()

    def __handle_events(self):
        """Handle PyGame events like exit or keypress."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_r:
                    self.map.reinit()
                    self.train.restart()

        return True

    def __draw(self):
        """Draw everything on screen from scratch."""
        self.screen.fill((255, 255, 255))

        # Track
        pygame.draw.lines(self.screen, (0, 0, 0), True, self.map.points, width=2)

        # Train
        train_position = self.map.distance_to_position(self.train.position)
        pygame.draw.circle(self.screen, (255, 0, 0), (train_position.x, train_position.y), 5)

        pygame.display.flip()
