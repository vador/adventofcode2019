from unittest import TestCase
from prog import Program

class TestProgram(TestCase):
    def test___str__(self):
        my_prog = Program([99])
        test = my_prog.__str__()
        print(test)
        self.assertEqual(test,"ip: 0[99]-[99]")
