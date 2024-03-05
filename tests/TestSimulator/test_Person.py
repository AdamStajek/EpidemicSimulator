import pytest
from sample.Simulator.Person import Person
from sample.Simulator.World import World


class TestPerson:
    testData = [
        (-1, 0),
        (3, 1),
        (6, 2),
        (16, 1),
        (18, 0)
    ]

    @pytest.mark.parametrize("daysSinceInfection, expected", testData)
    def test_evaluateState(self, daysSinceInfection, expected):
        person = Person()
        person.daysSinceInfection = daysSinceInfection
        person.evaluateState()
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
        world = World(100, 5)
        person = world.people[0]
        person.currentCoordinates = [1, 1]
        for i, coords in enumerate(world.getNeighboursCoordinates(1, 1)):
            world.map[coords[0]][coords[1]].sick += sickOrDeadInNeighbours[i]
        person.move(world)
        assert (person.currentCoordinates in expectedCoordinates)
