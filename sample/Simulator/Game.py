from sample.Simulator.World import World


class Game:
    """
    A class which instance represents the game.

    Attributes:
        day - current day in the game
        world - the world of the game
        infectedHistory - history of infections where infectedHistory[i] is number of infected at day i
        deadHistory - history of dead where deadHistory[i] is the number of dead at day i
        currentPopulationHistory - history of current population, analogical to dead and infected
    """
    def __init__(self, initialPopulation: int, worldSize: int, percentOfInitialInfected: int, transmissionRate: float,
                 deathRate: float):
        self._day: int = 0
        self._world: World = World(initialPopulation, worldSize, percentOfInitialInfected, transmissionRate, deathRate)
        self.infectedHistory: list[int] = []
        self.currentPopulationHistory: list[int] = []
        self.deadHistory: list[int] = []

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        self._world = value

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        self._day = value

    def startGame(self) -> None:
        """
        Stars the game.
        :return: None
        """
        self.world.distributePeople()
        self.world.initializeInfected()
        self.world.setDaysUntilMoving()

    def proceedDay(self) -> None:
        """
        Proceeds one day in the game
        :return: None
        """
        for person in self.world.people:
            person.evaluateState(self.world)
            if person.daysUntilMoving == 0:
                didMove = person.move(self.world)
                person.drawDaysUntilMoving()
                i, j = person.currentCoordinates
                if didMove and self.world.map[i][j].infected > 0:
                    person.DecideAboutGettingInfected(self.world)
            if not person.isHealthy():
                person.daysSinceInfection += 1
            person.daysUntilMoving -= 1
        self.updateDayStatistics()

    def updateDayStatistics(self) -> None:
        """
        Updates statistics of a day.
        :return: None
        """
        self.day += 1
        self.infectedHistory.append(self.world.infected)
        self.deadHistory.append(self.world.dead)
        self.currentPopulationHistory.append(self.world.currentPopulation)
