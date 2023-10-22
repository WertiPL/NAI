class Train:
    def __init__(self):
        self.position = 0
        self.speed = 0.2

    def restart(self):
        """Place train on start without any speed (initial state)."""

        self.position = 0

    def move(self, ticks):
        """Increment position and calculate other parameters based on elapsed time between main loop iterations."""

        self.position += ticks * self.speed
