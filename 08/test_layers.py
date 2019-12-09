from unittest import TestCase
from layers import Layers

class TestLayers(TestCase):
    def test_flatten_layers(self):
        my = Layers("0222112222120000",2,2)
        flat = (my.flatten_layers())
        res_expected = "0110"
        self.assertEqual(res_expected, flat.pixel_list)