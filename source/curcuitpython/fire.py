class Fire(object):
    """Control fire behavior."""
    def __init__(self, start, length):
        """Instantiate a fire object.

        Args:
            start (int): Starting index of fire LEDs.
            length (int): Total number of LEDs for fire.
        """
        self.start = start
        self.length = length
        self.wait = 0.1
        self.settings = {}
        self.initialize_settings()

    def adjust(self):
        return

    def initialize_settings():
        self.settings = {x: {"color": self.set_color(),
                             "transition_time": self.set_transition_time(),
                             "increasing": self.set_increasing(),
                             "increment": self.set_increment()}
                         for x in }
