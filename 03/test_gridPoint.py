from unittest import TestCase
from crosswire import GridPoint


class TestGridPoint(TestCase):
    def test_should_be_equal_same_point(self):
        orig = GridPoint(0,0)
        dest = GridPoint(0,0)
        self.assertEqual(orig, dest)

    def test_should_be_notequal_differents_points(self):
        orig = GridPoint(0,0)
        dest = GridPoint(1,1)
        self.assertNotEqual(orig, dest)
        orig = GridPoint(0,0)
        dest = GridPoint(0,1)
        self.assertNotEqual(orig, dest)
        orig = GridPoint(0,0)
        dest = GridPoint(1,0)
        self.assertNotEqual(orig, dest)


    def test_should_add_oney_when_move_up(self):
        orig = GridPoint(0,0)
        dest_expected = GridPoint(0,1)
        dest = orig.move_point_by_direction('U1')
        self.assertEqual(dest_expected, dest)

    def test_should_rmeove_y_when_move_down(self):
        orig = GridPoint(1, 5)
        dest_expected = GridPoint(1, 2)
        dest = orig.move_point_by_direction('D3')
        self.assertEqual(dest_expected, dest)

    def test_should_add_x_when_move_right(self):
        orig = GridPoint(1, 5)
        dest_expected = GridPoint(4, 5)
        dest = orig.move_point_by_direction('R3')
        self.assertEqual(dest_expected, dest)

    def test_should_remove_x_when_move_left(self):
        orig = GridPoint(1, 5)
        dest_expected = GridPoint(-14, 5)
        dest = orig.move_point_by_direction('L15')
        self.assertEqual(dest_expected, dest)
