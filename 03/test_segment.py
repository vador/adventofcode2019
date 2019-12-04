from unittest import TestCase
from crosswire import Segment
from crosswire import GridPoint



class TestSegment(TestCase):
    def test_intersect_colinear(self):
        orig = GridPoint(0,0)
        end = GridPoint(10,0)
        my_segment = Segment(orig,end)
        res_expected = [3,4,5]
        res = my_segment.intersect_colinear(2,5,3,7)
        self.assertEqual(res_expected, res)

    def test_intersect_segments_HH(self):
        seg1 = Segment(GridPoint(0,0), GridPoint(5,0))
        seg2 = Segment(GridPoint(3,0), GridPoint(15,0))
        res_expected = [(3,0),(4,0),(5,0)]
        res = seg1.intersection(seg2)
        self.assertEqual(res_expected, res)
        seg2 = Segment(GridPoint(3,1), GridPoint(15,1))
        res_expected = []
        res = seg1.intersection(seg2)
        self.assertEqual(res_expected, res)

