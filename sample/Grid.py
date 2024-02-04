class Grid:
    def __init__(self, x, y):
        self._infected: int = 0
        self._sick: int = 0
        self._dead: int = 0
        self._currentPopulation: int = 0
        self._coordinates: tuple[int, int] = (x, y)

    @property
    def infected(self):
        return self._infected

    @infected.setter
    def infected(self, value):
        self._infected = value

    @property
    def sick(self):
        return self._sick

    @sick.setter
    def sick(self, value):
        self._sick = value

    @property
    def dead(self):
        return self._dead

    @dead.setter
    def dead(self, value):
        self._dead = value

    @property
    def currentPopulation(self):
        return self._currentPopulation

    @currentPopulation.setter
    def currentPopulation(self, value):
        self._currentPopulation = value

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        self._coordinates = value




