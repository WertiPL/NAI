import pygame

MAP_MARGIN = 100


class Simulation:
    def __init__(self, game_map):
        """Initialize PyGame and all other resources."""
        self.map = game_map

        pygame.init()
        self.screen = pygame.display.set_mode([self.map.dimensions[0], self.map.dimensions[1] + MAP_MARGIN])

    def __del__(self):
        """On program end, cleanup resources."""
        pygame.quit()

    def run(self):
        """Main simulation loop that handles events and draws current data."""
        while True:
            if not self.__handle_events():
                break

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

        return True

    def __draw(self):
        """Draw everything on screen from scratch."""
        self.screen.fill((255, 255, 255))

        pygame.draw.lines(self.screen, (0, 0, 0), True, self.map.points, width=2)

        pygame.display.flip()
