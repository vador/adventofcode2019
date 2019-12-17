from unittest import TestCase
from prog3 import Program


class TestProgram(TestCase):
    def test_copy_itself(self):
        program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        my_prog = Program(program)
        my_prog_iter = my_prog.__iter__()
        values = []
        for val in my_prog_iter:
            values.append(val)
        self.assertEqual(program, values)

    def test_16_digit(self):
        program = [1102,34915192,34915192,7,4,7,99,0]
        res = [1219070632396864]
        my_prog = Program(program)
        my_prog_iter = my_prog.__iter__()
        values = []
        for val in my_prog_iter:
            values.append(val)
        self.assertEqual(res, values)

    def test_output_digit(self):
        program = [104,1125899906842624,99]
        res = [1125899906842624]
        my_prog = Program(program)
        my_prog_iter = my_prog.__iter__()
        values = []
        for val in my_prog_iter:
            values.append(val)
        self.assertEqual(res, values)
