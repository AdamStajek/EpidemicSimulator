import random
from sample.Simulator.Grid import Grid


class World:
    """
    A class which represents the world of the game.
    """
    def __init__(self, initialPopulation: int, worldSize: int, percentOfInitialInfected: int, transmissionRate: float, deathRate: float):
        """
        Constructs a World class instance.
        :param initialPopulation: initial population of the world
        :param worldSize: world size
        """
        self._initialPopulation: int = initialPopulation
        self._currentPopulation: int = initialPopulation
        self._worldSize: int = worldSize
        self._percentOfInitialInfected: int = percentOfInitialInfected
        self._transmissionRate: float = transmissionRate
        self._deathRate: float = deathRate
        self._infected: int = 0
        self._sick: int = 0
        self._dead: int = 0
        self._map: list = [[None for x in range(worldSize)] for y in range(worldSize)]
        self._people: list[Person] = [Person() for x in range(initialPopulation)]
        for i in range(worldSize):
            for j in range(worldSize):
                self._map[i][j] = Grid(i, j)

    @property
    def initialPopulation(self):
        return self._initialPopulation

    @initialPopulation.setter
    def initialPopulation(self, value):
        self._initialPopulation = value

    @property
    def worldSize(self):
        return self._worldSize

    @worldSize.setter
    def worldSize(self, value):
        self._worldSize = value

    @property
    def percentOfInitialInfected(self):
        return self._percentOfInitialInfected

    @percentOfInitialInfected.setter
    def percentOfInitialInfected(self, value):
        self._percentOfInitialInfected = value

    @property
    def transmissionRate(self):
        return self._transmissionRate

    @transmissionRate.setter
    def transmissionRate(self, value):
        self._transmissionRate = value

    @property
    def deathRate(self):
        return self._deathRate

    @deathRate.setter
    def deathRate(self, value):
        self._deathRate = value

    @property
    def infected(self):
        return self._infected

    @infected.setter
    def infected(self, value):
        self._infected = value

    @property
    def dead(self):
        return self._dead

    @dead.setter
    def dead(self, value):
        self._dead = value

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, value):
        self._map = value

    @property
    def people(self):
        return self._people

    @people.setter
    def people(self, value):
        self._people = value

    @property
    def currentPopulation(self):
        return self._currentPopulation

    @currentPopulation.setter
    def currentPopulation(self, value):
        self._currentPopulation = value

    @property
    def sick(self):
        return self._sick

    @sick.setter
    def sick(self, value):
        self._sick = value

    def initializeInfected(self) -> None:
        """
        Makes specified number of people infected on different disease stage
        :return: None
        """
        for i in range(int(self.percentOfInitialInfected / 100 * self.initialPopulation)):
            person = self._people[i]
            person.getInfected(self)  # TODO test
            person.daysSinceInfection = self.drawDaysSinceInfection()
            if person.daysSinceInfection >= 6:
                person.getSick(self)

    def drawDaysSinceInfection(self) -> int:
        """
        returns random days since infection from 0 to 10
        :return:
        """
        return random.randint(0, 10)

    def distributePeople(self) -> None:
        """
        Distributes people uniformly random around the world
        :return: None
        """
        for person in self.people:
            i, j = random.randint(0, self.worldSize - 1), random.randint(0, self.worldSize - 1)
            person.currentCoordinates = i, j
            self.map[i][j].currentPopulation += 1

    def setDaysUntilMoving(self):
        for person in self.people:
            person.drawDaysUntilMoving()

    def getNeighboursCoordinates(self, i: int, j: int) -> list[[int, int]]:
        """
        Finds neighbours coordinate of a grid.
        :param i: x coordinate of the grid which neighbours we want to find
        :param j: y coordinate of the grid which neighbours we want to find
        :return: None
        """
        neighboursCoordinates = [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]
        self._ensureCyclicWorld(neighboursCoordinates)
        return neighboursCoordinates

    def _ensureCyclicWorld(self, neighboursCoordinates: list[(int, int)]) -> None:
        """
        Ensures that the world is cyclic.
        :param neighboursCoordinates: coordinates of the grids, which we want to check if they are in the world
        :return: None
        """
        for coord in neighboursCoordinates:
            if coord[0] == -1:
                coord[0] = len(self.map) - 1
            elif coord[0] == len(self.map):
                coord[0] = 0

            if coord[1] == -1:
                coord[1] = len(self.map) - 1
            elif coord[1] == len(self.map):
                coord[1] = 0




from sample.Simulator.Person import Person
