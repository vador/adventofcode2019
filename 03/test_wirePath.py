from unittest import TestCase
from crosswire import WirePath
from crosswire import Segment
from crosswire import GridPoint


class TestWirePath(TestCase):
    def test_is_val_between(self):
        wp = WirePath("R8,U5,L5,D3")
        self.assertTrue(wp.is_val_between(3, 1, 5))
        self.assertTrue(wp.is_val_between(3, 5, 3))
        self.assertFalse(wp.is_val_between(1, 3, 5))
        self.assertFalse(wp.is_val_between(1, 5, 3))
        self.assertFalse(wp.is_val_between(6, 5, 3))
        self.assertFalse(wp.is_val_between(1, 5, 3))

    def test_is_cell_on_segment(self):
        wp = WirePath("R8,U5,L5,D3")
        point = GridPoint(1, 1)
        orig = GridPoint(-1, 1)
        dest = GridPoint(15, 1)
        self.assertTrue(wp.is_cell_on_segment(point, orig, dest))
        point = GridPoint(1, 1)
        orig = GridPoint(1, -1)
        dest = GridPoint(1, 10)
        self.assertTrue(wp.is_cell_on_segment(point, orig, dest))
        point = GridPoint(1, 100)
        self.assertFalse(wp.is_cell_on_segment(point, orig, dest))

    def test_is_cell_on_path(self):
        wp = WirePath("R8,U5,L5,D3")
        point = GridPoint(6, 0)
        self.assertTrue(wp.is_cell_on_path(point))
        point = GridPoint(3, 3)
        self.assertTrue(wp.is_cell_on_path(point))
        point = GridPoint(4, 3)
        self.assertFalse(wp.is_cell_on_path(point))

    def test_get_segments(self):
        wp = WirePath("R8,U5,L5,D3")
        res_expected = [Segment(GridPoint(0, 0), GridPoint(8, 0)),
                        Segment(GridPoint(8, 0), GridPoint(8, 5)),
                        Segment(GridPoint(3, 5), GridPoint(8, 5)),
                        Segment(GridPoint(3, 2), GridPoint(3, 5)),
                        ]
        res = wp.get_segments()
        self.assertEqual(res_expected, res)

    def test_steps_to_cell(self):
        wp = WirePath("R8,U5,L5,D3")
        point = GridPoint(3,3)
        res_expected = 20
        res = wp.steps_to_cell(point)
        self.assertEqual(res_expected, res)