import math
from random import randint
from shapely import LineString


class Map:
    def __init__(self, dimensions, turns=3):
        self.points = []
        self.dimensions = dimensions
        self.turns = turns
        self.length = 0

        self.__generate_points()

    def reinit(self):
        """Recreate random map."""
        self.points = []
        self.__generate_points()

    def distance_to_position(self, distance):
        """Get XY coordinates by given distance on track."""

        points = self.points
        # unnecessary to delete
        # points.append(self.points[0])

        line = LineString(points)

        distance = distance % self.length

        return line.interpolate(distance)



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

        self.__calculate_length()

    def __calculate_length(self):
        """Calculate total track length, in pixels."""

        points = self.points
        # unnecessary to delete
        # points.append(self.points[0])

        line = LineString(points)

        self.length = int(line.length)

