import math
from random import randint


class Map:
    def __init__(self, dimensions, turns=3):
        self.points = []
        self.dimensions = dimensions
        self.turns = turns

        self.__generate_points()

    def reinit(self):
        """Recreate random map."""
        self.points = []
        self.__generate_points()

    def __generate_points(self):
        """Generate random map points that are not too close to each other."""

        while len(self.points) < self.turns:
            x = randint(0, self.dimensions[0])
            y = randint(0, self.dimensions[1])

            valid = True

            for point in self.points:
                dist = math.dist((x, y), point)

                if dist < (self.dimensions[0] + self.dimensions[1]) / 4:
                    valid = False
                    break

            if valid:
                self.points.append((x, y))
