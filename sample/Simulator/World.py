from sample.Simulator.Grid import Grid
import sample.Simulator.Person as Person_


class World:
    def __init__(self, initialPopulation: int, worldSize: int):
        self._initialPopulation: int = initialPopulation
        self._infected: int = 0
        self._dead: int = 0
        self._map: list = [[None for x in range(worldSize)] for y in range(worldSize)]
        self._people: list[Person_.Person] = [Person_.Person() for x in range(initialPopulation)]
        for i in range(worldSize):
            for j in range(worldSize):
                self._map[i][j] = Grid(i, j)

    def initializeInfected(self, percentOfInitialInfected: int) -> None:
        for i in range(int(percentOfInitialInfected/100 * self.initialPopulation)):
            person = self._people[i]
            person.getInfected() #TODO test

    @property
    def initialPopulation(self):
        return self._initialPopulation

    @initialPopulation.setter
    def initialPopulation(self, value):
        self._initialPopulation = value

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

    def getNeighboursCoordinates(self, i: int, j: int) -> list[[int, int]]:
        neighboursCoordinates = [[i+1, j], [i-1, j], [i, j+1], [i, j-1]]
        self._ensureCyclicWorld(neighboursCoordinates)
        return neighboursCoordinates

    def _ensureCyclicWorld(self, neighboursCoordinates: list[(int, int)]) -> None:
        for coord in neighboursCoordinates:
            if coord[0] == -1:
                coord[0] = len(self.map) - 1
            elif coord[0] == len(self.map):
                coord[0] = 0

            if coord[1] == -1:
                coord[1] = len(self.map) - 1
            elif coord[1] == len(self.map):
                coord[1] = 0





