from random import Random
from sample.Simulator.World import World
from sample.Simulator.Grid import Grid


class Person:
    """
    A class which represents one person in the world.

    Attributes:
        daysSinceInfection - days since the person got infected
        isDead - if the person is dead
        state - current state of the person:
            0 - healthy
            1 - infected
            2 - sick
            3 - dead
        daysUntilMoving - number of days until person's move
        currentCoordinates - coordinates of the grid where the person is now
    """
    def __init__(self):
        """
        Constructs class Person.
        """
        self._daysSinceInfection: int = -1
        self._isDead: bool = False
        self._state: int = 0
        self._daysUntilMoving: int = 1000
        self._currentCoordinates: list[int, int] = [-1, -1]

    @property
    def daysSinceInfection(self):
        return self._daysSinceInfection

    @daysSinceInfection.setter
    def daysSinceInfection(self, value):
        self._daysSinceInfection = value

    @property
    def isDead(self):
        return self._isDead

    @isDead.setter
    def isDead(self, value):
        self._isDead = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def daysUntilMoving(self):
        return self._daysUntilMoving

    @daysUntilMoving.setter
    def daysUntilMoving(self, value):
        self._daysUntilMoving = value

    @property
    def currentCoordinates(self):
        return self._currentCoordinates

    @currentCoordinates.setter
    def currentCoordinates(self, value):
        self._currentCoordinates = value

    def isHealthy(self):
        return self.daysSinceInfection == -1

    def drawDaysUntilMoving(self) -> None:
        """
        Draws days until moving from one to five and assigns it to the attribute daysUntilMoving.
        :return: None
        """
        self.daysUntilMoving = Random().randint(1, 5)

    def move(self, world: World) -> bool:
        """
        Simulates person move
        :param world: the world
        :return: True if person has moved and False otherwise
        """
        if self.isDead:
            return False
        neighboursCoordinates = world.getNeighboursCoordinates(*self._currentCoordinates)
        neighboursCoordinates = self._excludeCountriesWithSickPeople(neighboursCoordinates, world)
        if len(neighboursCoordinates) == 0:
            return False
        newGrid = neighboursCoordinates[self._drawGridToMove(neighboursCoordinates)]
        self.currentCoordinates = newGrid
        return True

    def _excludeCountriesWithSickPeople(self, neighboursCoordinates: list[[int, int]],
                                        world: World) -> list[[int, int]]:
        """
        Exclude neighbours with sick people from possible moving areas.
        :param neighboursCoordinates: map coordinates of the neighbours of the grid which person is in
        :param world: the world
        :return: list of neighbours coordinates valid to move to
        """
        new_neighbours = []
        for coord in neighboursCoordinates:
            neighbour: Grid = world.map[coord[0]][coord[1]]
            if neighbour.sick == 0 and neighbour.currentPopulation != 0:
                new_neighbours.append(neighbour.coordinates)
        return new_neighbours

    def _drawGridToMove(self, neighboursCoordinates: list[[int, int]]) -> int:
        """
        Draws one grid from possible moving grids.
        :param neighboursCoordinates: list of neighbours coordinates valid to move to
        :return: index of the drawed neighbour in the neighbour coordinates list
        """
        return Random().randint(0, len(neighboursCoordinates) - 1)

    @classmethod
    def _drewNumberFrom0to1(cls) -> float:
        """
        Draws number of 0 to 1.
        :return: float number in the interval [0, 1)
        """
        return Random().random()

    def decideAboutDeath(self, world: World) -> None:
        """
        Decide if person dies.
        :param world: the world
        :return: None
        """
        drewNumber = Person._drewNumberFrom0to1()
        if drewNumber < world.deathRate:
            self.die(world)

    def die(self, world: World) -> None:
        """
        Simulates the death of the person
        :param world: the world
        :return: None
        """
        self.isDead = True
        self.daysSinceInfection = -1
        self.state = 3
        self._updateStatisticsAfterDeath(world)

    def _updateStatisticsAfterDeath(self, world: World) -> None:
        """
        Updates statistics after person's death
        :param world: the world
        :return: None
        """
        i, j = self.currentCoordinates
        world.currentPopulation -= 1
        world.infected -= 1
        world.sick -= 1
        world.dead += 1
        world.map[i][j].currentPopulation -= 1
        world.map[i][j].infected -= 1
        world.map[i][j].sick -= 1
        world.map[i][j].dead += 1

    def DecideAboutGettingInfected(self, world: World) -> None:
        """
        Decide if person gets infected.
        :param world: the world
        :return: None
        """
        if self.state != 0:
            return
        drewNumber = Person._drewNumberFrom0to1()
        if drewNumber < world.transmissionRate:
            self.getInfected(world)

    def getInfected(self, world: World) -> None:
        """
        Simulates the infection of the person
        :param world: the world
        :return: None
        """
        self.daysSinceInfection = 0
        self.state = 1
        self._updateStatisticsAfterInfection(world)

    def _updateStatisticsAfterInfection(self, world: World) -> None:
        """
        Updates statistics after person's getting infected
        :param world: the world
        :return: None
        """
        i, j = self.currentCoordinates
        world.infected += 1
        world.map[i][j].infected += 1

    def getSick(self, world: World) -> None:
        """
        Simulates getting sick of the person
        :param world: the world
        :return: None
        """
        self.state = 2
        self._updateStatisticsAfterGettingSick(world)

    def _updateStatisticsAfterGettingSick(self, world: World) -> None:
        """
        Updates statistics after person's getting sick
        :param world: the world
        :return: None
        """
        i, j = self.currentCoordinates
        world.sick += 1
        world.map[i][j].sick += 1

    def becomeImmune(self, world: World) -> None:
        """
        Simulates becoming immune of the person
        :param world: the world
        :return: None
        """
        self.state = 1
        self._updateStatisticsAfterBecomingImmune(world)

    def _updateStatisticsAfterBecomingImmune(self, world: World) -> None:
        """
        Updates statistics after person's becoming immune
        :param world: the world
        :return: None
        """
        i, j = self.currentCoordinates
        world.sick -= 1
        world.map[i][j].sick -= 1

    def getWell(self, world: World) -> None:
        """
        Simulates the getting well of the person
        :param world: the world
        :return: None
        """
        self.state = 0
        self.daysSinceInfection = -1
        self._updateStatisticsAfterGettingWell(world)

    def _updateStatisticsAfterGettingWell(self, world: World) -> None:
        """
        Updates statistics after person's getting well
        :param world: the world
        :return: None
        """
        i, j = self.currentCoordinates
        world.infected -= 1
        world.map[i][j].sick -= 1

    def evaluateState(self, world: World) -> None:
        """
        Changes state of the person on the specific days after getting infected
        :param world: the world
        :return: None
        """
        if self.isDead:
            return
        if self.daysSinceInfection == 6:
            self.getSick(world)
        if self.daysSinceInfection == 14:
            self.decideAboutDeath(world)
        if self.daysSinceInfection == 16:
            self.becomeImmune(world)
        if self.daysSinceInfection == 18:
            self.getWell(world)
