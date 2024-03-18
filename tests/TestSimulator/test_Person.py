import pytest
from sample.Simulator.World import World


class TestPerson:
    testData = [
        (0, 1),
        (6, 2),
        (18, 0)
    ]

    @pytest.mark.parametrize("daysSinceInfection, expected", testData)
    def test_evaluateState(self, daysSinceInfection, expected):
        world = World(1000, 5, 10, 0.8, 0.2)
        person = Person()
        person.getInfected(world)
        person.daysSinceInfection = daysSinceInfection
        person.evaluateState(world)
        assert person.state == expected

    def test_drawDaysUntilMoving(self):
        person = Person()
        person.drawDaysUntilMoving()
        assert 1 <= person.daysUntilMoving <= 5

    testData = [
        ([0, 0, 0, 0], [[0, 1], [2, 1], [1, 2], [1, 0]]),
        ([0, 1, 1, 0], [[2, 1], [1, 0]]),
        ([1, 1, 1, 1], [[1, 1]])
    ]

    @pytest.mark.parametrize("sickOrDeadInNeighbours, expectedCoordinates", testData)
    def test_move(self, sickOrDeadInNeighbours, expectedCoordinates):
        world = World(1000, 5, 10, 0.8, 0.2)
        world.distributePeople()
        person = world.people[0]
        person.currentCoordinates = [1, 1]
        for i, coords in enumerate(world.getNeighboursCoordinates(1, 1)):
            world.map[coords[0]][coords[1]].sick += sickOrDeadInNeighbours[i]
        person.move(world)
        assert (person.currentCoordinates in expectedCoordinates)




from sample.Simulator.Person import Person