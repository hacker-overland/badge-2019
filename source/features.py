"""Drive feature states here."""


class LightFader:
    """Generic light fader."""

    seq_len = 0
    color_ref = {}
    floor = (0, 0, 0)

    def __init__(self, level, indexen):
        """Initialize with level and LED indexes.

        Args:
            level (int): Level of intensity.
            indexen (list): List of integers indicating feature's LED indexes.
        """
        self.level = level
        self.indexen = indexen
        self.current = (0, 0, 0)

    def generator(self):
        """Yield feature's next state values."""
        up_direction = True
        full_color = self.color_ref[self.level]
        incrementer = tuple(x / self.seq_len for x in full_color)
        while True:
            if up_direction:
                self.current = tuple(self.current[x] + incrementer[x]
                                     for x in range(3))
                up_direction = max(self.current) < max(full_color)
            else:
                self.current = tuple(self.current[x] - incrementer[x]
                                     for x in range(3))
                up_direction = max(self.current) < max(self.floor)
            yield {x: self.current for x in self.indexen}


class LightFlasher:
    """Generic light flasher."""

    seq_len = 0
    color_ref = {}
    floor = (0, 0, 0)

    def __init__(self, level, indexen):
        """Initialize with level and indexen.

        Args:
            level (int): Level of intensity.
            indexen (list): List of integers indicating feature's LED indexes.
        """
        self.level = level
        self.indexen = indexen
        self.current = (0, 0, 0)

    def generator(self):
        """Yield feature's next state values."""
        while True:
            for x in range(self.seq_len):
                yield {x: self.floor for x in self.indexen}
            for x in range(self.seq_len):
                yield {x: self.color_ref[self.level] for x in self.indexen}


class Raccoon(LightFader):
    """Raccoon feature."""

    seq_len = 100
    floor = (2, 4, 0)
    color_ref = {0: (0, 0, 0),
                 1: (2, 4, 0),
                 2: (4, 8, 0),
                 3: (8, 16, 0),
                 4: (16, 32, 0)}


class Bat(LightFader):
    """Bat feature."""
    seq_len = 10
    floor = (0, 2, 0)
    color_ref = {0: (0, 0, 0),
                 1: (0, 4, 0),
                 2: (0, 8, 0),
                 3: (0, 16, 0),
                 4: (0, 32, 0)}

class Truck(LightFlasher):
    """Truck feature."""
    seq_len = 30
    color_ref = {0: (0, 0, 0),
                 1: (0, 4, 0),
                 2: (0, 8, 0),
                 3: (0, 16, 0),
                 4: (0, 32, 0)}

class Smoke(LightFader):
    """Smoke feature."""
    floor = (8, 8, 0)
    seq_len = 65
    color_ref = {0: (0, 0, 0),
                 1: (8, 8, 8),
                 2: (16, 16, 16),
                 3: (32, 32, 32),
                 4: (64, 64, 64)}
