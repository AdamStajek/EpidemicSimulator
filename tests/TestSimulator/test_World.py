import pytest
from sample.Simulator.World import World


class TestWorld:
    NeighboursTestData = [
        ((1, 2), 5, [[2, 2], [0, 2], [1, 3], [1, 1]], False),
        ((0, 3), 4, [[1, 3], [3, 3], [0, 0], [0, 2]], False),
        ((0, 6), 5, pytest.raises(ValueError), True)
    ]

    @pytest.mark.parametrize("neighboursCoordinates, worldSize, expected, raisesError", NeighboursTestData)
    def test_GetNeighboursCoordinates(self, neighboursCoordinates, worldSize, expected, raisesError):
        if raisesError:
            assert pytest.raises(ValueError)
        else:
            world = World(300, worldSize, 10, 0.8, 0.2)
            newCoords = world.getNeighboursCoordinates(*neighboursCoordinates)
            assert newCoords == expected

    def test_initializeInfected(self):
        initialPopulation = 1000
        percentOfInitialInfected = 10
        world = World(initialPopulation, 10, percentOfInitialInfected, 0.8, 0.2)
        world.initializeInfected()
        count = 0
        for person in world.people:
            if person.state in (1, 2):
                count += 1
        assert count == 100

    def test_distributePeople(self):
        initialPopulation = 1000
        world = World(initialPopulation, 10, 10, 0.8, 0.2)
        world.distributePeople()
        count = 0
        for grids in world.map:
            for grid in grids:
                count += grid.currentPopulation
        assert count == 1000
