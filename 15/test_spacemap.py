from unittest import TestCase
from spacemap import SpaceMap


class TestSpaceMap(TestCase):
    def test_turn_right(self):
        my_sp = SpaceMap()
        direction = 'N'
        self.assertEqual('E', my_sp.turnRight(direction))
        direction = 'E'
        self.assertEqual('S', my_sp.turnRight(direction))
        direction = 'S'
        self.assertEqual('W', my_sp.turnRight(direction))
        direction = 'W'
        self.assertEqual('N', my_sp.turnRight(direction))


    def test_turn_left(self):
        my_sp = SpaceMap()
        direction = 'N'
        self.assertEqual('W', my_sp.turnLeft(direction))
        direction = 'E'
        self.assertEqual('N', my_sp.turnLeft(direction))
        direction = 'S'
        self.assertEqual('E', my_sp.turnLeft(direction))
        direction = 'W'
        self.assertEqual('S', my_sp.turnLeft(direction))

    def test_coming_from(self):
        my_sp = SpaceMap()
        direction = 'N'
        self.assertEqual('S', my_sp.coming_from(direction))
