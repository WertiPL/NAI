import math

import pygame

MAP_MARGIN = 100
FONT_COLOR = (0, 0, 0)
OBJECT_COLOR = (0, 0, 255)


class Simulation:
    def __init__(self, game_map, train, controller):
        """Initialize PyGame and all other resources."""
        self.map = game_map
        self.train = train
        self.braking_controller = controller

        pygame.init()
        self.screen = pygame.display.set_mode(
            size=[self.map.dimensions[0], self.map.dimensions[1] + MAP_MARGIN],
            flags=pygame.SCALED,
            vsync=1
        )

        pygame.display.set_caption("Automatic Braking System Simulation")

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
            # Check Way before move is it turn?

            angle_deg = self.__angle_between_vectors(self.map.distance_to_position(self.train.position))
            absolute_distance, relative_distance = self.find_closest_vertex(self.map.points)

            print(f"Absolute Distance to Closest Vertex: {absolute_distance}")
            print(f"Relative Distance to Turn: {relative_distance}")
            if angle_deg != 0 or angle_deg > 10:
                if angle_deg < 0:
                    angle_deg = angle_deg * -1
                distance_to_turn = relative_distance
                angle_of_turn = angle_deg
                speed_of_train = self.train.speed
                if 800 > distance_to_turn > 0 and 0 < speed_of_train < 5 and 0 < angle_deg < 180:
                    braking_force = self.braking_controller.compute(distance_to_turn, angle_of_turn, speed_of_train)
                else:
                    braking_force = 0
            else:
                braking_force = 0
            self.train.move(time_delta, braking_force)

            self.__draw()

            if self.train.position > self.map.length:
                self.train.reset_position()

            print(f".")

    def find_closest_vertex(self, vertices):
        total_distance = 0
        previous_vertex = vertices[0]
        vertices.append(previous_vertex)
        for vertex in vertices:
            # Calculate the distance between the current and previous vertices
            distance = math.sqrt((vertex[0] - previous_vertex[0]) ** 2 + (vertex[1] - previous_vertex[1]) ** 2)

            # Check if the total distance exceeds the train's position
            if total_distance + distance > self.train.position:
                # Calculate the absolute distance to the closest vertex
                absolute_distance = self.train.position - total_distance

                # Calculate the relative (remaining) distance to the turn
                remaining_distance = distance - absolute_distance

                return absolute_distance, remaining_distance

            total_distance += distance
            previous_vertex = vertex

        return 0, 0

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

        #  Displaying speed of Train
        font = pygame.font.Font(None, 28)
        speed_text = font.render(f"Speed: {self.train.speed:.2f}", True, FONT_COLOR)
        self.screen.blit(speed_text, (10, 10))

        pygame.display.flip()

    def __angle_between_vectors(self, vector2):
        # Calculate the dot product of two vectors
        dot_product = self.train.position * vector2.x + self.train.position * vector2.y

        # Calculate the magnitude (length) of the first vector
        magnitude1 = math.sqrt(self.train.position ** 2 + self.train.position ** 2)

        # Calculate the magnitude (length) of the second vector
        magnitude2 = math.sqrt(vector2.x ** 2 + vector2.y ** 2)

        # Check if one of the vectors is zero (undefined angle)
        if magnitude1 == 0 or magnitude2 == 0:
            # One of the vectors is zero, and the angle is undefined
            return 0  # or another value representing an undefined angle

        # Check if the dot product is very close to zero (almost perpendicular vectors)
        if abs(dot_product) < 1e-10:
            # The dot product is very close to zero, treat it as nearly perpendicular vectors (90 degrees)
            return 90  # or another value representing a 90-degree angle

        # Calculate the angle in radians between the two vectors using the dot product
        angle_rad = math.acos(max(-1, min(1, dot_product / (magnitude1 * magnitude2))))

        # Convert the angle from radians to degrees
        angle_deg = math.degrees(angle_rad)
        return angle_deg

