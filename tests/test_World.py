import pytest
from sample.World import World


class TestWorld:
    NeighboursTestData = [
        ((1, 2), 5, [[2, 2], [0, 2], [1, 3], [1, 1]], False),
        ((0, 3), 4, [[1, 3], [3, 3], [0, 0], [0, 2]], False),
        ((0, 6), 5, pytest.raises(ValueError), True)
    ]

    @pytest.mark.parametrize("neighboursCoordinates,worldSize,expected, raisesError", NeighboursTestData)
    def test_GetNeighboursCoordinates(self, neighboursCoordinates, worldSize, expected, raisesError):
        if raisesError:
            assert pytest.raises(ValueError)
        else:
            world = World(300, worldSize)
            newCoords = world.getNeighboursCoordinates(*neighboursCoordinates)
            assert newCoords == expected
