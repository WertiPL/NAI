class Train:
    def __init__(self):
        self.position = 0
        self.acceleration = 0.2
        self.speed = 0

    def restart(self):
        """Place train on start without any speed (initial state)."""

        self.speed = 0
        self.acceleration = 0.2
        self.position = 0

    def move(self, ticks, brake):
        """Increment position and calculate other parameters based on elapsed time between main loop iterations."""
        self.speed = ticks * (self.acceleration - brake)
        self.position += self.speed

    def auto_brake(self):
        """Here will auto brake"""
        self.acceleration -= 0.2

    def reset_position(self):
        self.position = 0
