from random import Random
import sample.World as World_


class Person:
    def __init__(self):
        """
        daysSinceInfection:
        -1 - healthy

        state:
        0 - healthy
        1 - infected
        2 - sick
        3 - dead

        """
        self._daysSinceInfection: int = -1
        self._isDead: bool = False
        self._state: int = 0
        self._daysUntilMoving: int = 1000
        self._currentCoordinates: tuple[int, int] = (-1, -1)

    @property
    def daysSinceInfection(self):
        return self._daysSinceInfection

    @daysSinceInfection.setter
    def daysSinceInfection(self, value):
        self.daysSinceInfection = value

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
    def daysUntilMoving(self,  value):
        self._daysUntilMoving = value

    @property
    def currentCoordinates(self):
        return self._currentCoordinates

    @currentCoordinates.setter
    def currentCoordinates(self, value):
        self._currentCoordinates = value

    def evaluateState(self) -> int | None:
        if self.isDead:
            return
        if self.daysSinceInfection == -1:
            self.state = 0
        elif 0 <= self.daysSinceInfection <= 5:
            self.state = 1
        elif 6 <= self.daysSinceInfection <= 15:
            self.state = 2
        elif 16 <= self.daysSinceInfection <= 17:
            self.state = 1
        elif self.daysSinceInfection == 18:
            self.state = 0
            self.daysSinceInfection = -1

    def dieOrNot(self) -> None:
        drewNumber = Person._drewNumberFrom0to1()
        if drewNumber < 0.25:
            self.isDead = True
            self.daysSinceInfection = -1

    def drawDaysUntilMoving(self) -> None:
        self.daysUntilMoving = Random().randint(1, 5)

    def move(self, world: World_) -> None:
        neighboursCoordinates = world.getNeighboursCoordinates(*self._currentCoordinates)
        neighboursCoordinates = self._excludeCountriesWithSickOrDeadPeople(neighboursCoordinates, world)
        if len(neighboursCoordinates) == 0:
            return
        newGrid = neighboursCoordinates[self._drawGridToMove(neighboursCoordinates)]
        self.currentCoordinates = newGrid

    def _excludeCountriesWithSickOrDeadPeople(self, neighboursCoordinates: list[[int, int]], world: World_) -> list[[int, int]]:
        new_neighbours = []
        for coord in neighboursCoordinates:
            neighbour = world.map[coord[0]][coord[1]]
            if neighbour.sick == 0 and neighbour.dead == 0:
                new_neighbours.append(neighbour)
        return new_neighbours

    def _drawGridToMove(self, neighboursCoordinates: list[[int, int]]) -> int:
        return Random().randint(0, len(neighboursCoordinates) - 1)

    def _getInfectedOrNot(self) -> None:
        drewNumber = Person._drewNumberFrom0to1()
        if drewNumber < 0.4:
            self.getInfected()

    def getInfected(self) -> None:
        self.daysSinceInfection = 0
        self.state = 1

    @classmethod
    def _drewNumberFrom0to1(cls) -> float:
        return Random().random()
