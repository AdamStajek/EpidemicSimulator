from sample.Simulator.World import World


class Game:
    def __init__(self, initialPopulation, worldSize, percentOfInitialInfected):
        self._initialPopulation = initialPopulation
        self._worldSize = worldSize
        self._percentOfInitialInfected = percentOfInitialInfected
        self._day = 0
        self._world: World = None

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

    def startGame(self):
        self.world = World(self.initialPopulation, self.worldSize)
        self.world.initializeInfected(self.percentOfInitialInfected)
        self.world.distributePeople(self.worldSize)
        for person in self.world.people:
            person.drawDaysUntilMoving()

    def proceedDay(self):
        for person in self.world.people:
            if person.daysUntilMoving == 0:
                didMove = person.move(self.world)
                if didMove:
                    person.getInfectedOrNot()
        self.day += 1





