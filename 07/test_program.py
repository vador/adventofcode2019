from unittest import TestCase
from prog import Program


class TestProgram(TestCase):

    def test_parse_paramopcode(self):
        pr = Program(["1022,1,2,3"])
        res_expected = (2, 0, 1, 0)
        res = pr.parse_paramopcode(1002)
        self.assertEqual(res_expected, res)
        res_expected = (2, 0, 1, 1)
        res = pr.parse_paramopcode(1102)
        self.assertEqual(res_expected, res)
        res_expected = (2, 1, 0, 0)
        res = pr.parse_paramopcode(10002)
        self.assertEqual(res_expected, res)

    def test_equals_pos(self):
        str_value = "3,9,8,9,10,9,4,9,99,-1,8"
        l_values = list(map(int, str_value.split(",")))
        pr = Program(l_values)
        pr.input = [4]
        pr.evaluate()
        res = pr.output
        res_expected = [0]
        self.assertEqual(res_expected, res)
        pr = Program(l_values)
        pr.input = [8]
        pr.evaluate()
        res = pr.output
        res_expected = [1]
        self.assertEqual(res_expected, res)

    def test_lt_pos(self):
        str_value = "3,9,7,9,10,9,4,9,99,-1,8"
        l_values = list(map(int, str_value.split(",")))
        pr = Program(l_values)
        pr.input = [4]
        pr.evaluate()
        res = pr.output
        res_expected = [1]
        self.assertEqual(res_expected, res)
        pr = Program(l_values)
        pr.input = [8]
        pr.evaluate()
        res = pr.output
        res_expected = [0]
        self.assertEqual(res_expected, res)
        pr.input = [9]
        pr.evaluate()
        res = pr.output
        res_expected = [0]
        self.assertEqual(res_expected, res)

    def test_equals_imm(self):
        str_value = "3,3,1108,-1,8,3,4,3,99"
        l_values = list(map(int, str_value.split(",")))
        pr = Program(l_values)
        pr.input = [9]
        pr.evaluate()
        res = pr.output
        res_expected = [0]
        self.assertEqual(res_expected, res)
        pr = Program(l_values)
        pr.input = [8]
        pr.evaluate()
        res = pr.output
        res_expected = [1]
        self.assertEqual(res_expected, res)

    def test_lt_imm(self):
        str_value = "3,3,1107,-1,8,3,4,3,99"
        l_values = list(map(int, str_value.split(",")))
        pr = Program(l_values)
        pr.input = [4]
        pr.evaluate()
        res = pr.output
        res_expected = [1]
        self.assertEqual(res_expected, res)
        pr = Program(l_values)
        pr.input = [8]
        pr.evaluate()
        res = pr.output
        res_expected = [0]
        self.assertEqual(res_expected, res)
        pr.input = [9]
        pr.evaluate()
        res = pr.output
        res_expected = [0]
        self.assertEqual(res_expected, res)

    def test_jmp_pos(self):
        str_value = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
        l_values = list(map(int, str_value.split(",")))
        pr = Program(l_values)
        pr.input = [0]
        pr.evaluate()
        res = pr.output
        res_expected = [0]
        self.assertEqual(res_expected, res)
        pr = Program(l_values)
        pr.input = [8]
        pr.evaluate()
        res = pr.output
        res_expected = [1]
        self.assertEqual(res_expected, res)

    def test_jmp_imm(self):
        str_value = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
        l_values = list(map(int, str_value.split(",")))
        pr = Program(l_values)
        pr.input = [0]
        pr.evaluate()
        res = pr.output[0]
        res_expected = 0
        self.assertEqual(res_expected, res)
        pr = Program(l_values)
        pr.input = [8]
        pr.evaluate()
        res = pr.output[0]
        res_expected = 1
        self.assertEqual(res_expected, res)


    def test_jumps(self):
        str_value = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31," + \
                    "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104," + \
                    "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        l_values = list(map(int, str_value.split(",")))
        pr = Program(l_values)
        pr.input = [6]
        pr.evaluate()
        res = pr.output[0]
        res_expected = 999
        self.assertEqual(res_expected, res)
