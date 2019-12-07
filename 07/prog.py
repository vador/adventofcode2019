import sys
import re
import collections
import math
import heapq


class LoadValues:
    file = './input'
    raw_values = None
    processed_values = None

    def __init__(self, data=None, file=True):
        if file:
            if data is not None:
                file_name = data
            else:
                file_name = self.file
            with open(file_name) as f:
                self.raw_values = list(f)
        else:
            self.raw_values = list(data)

    def list_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = [int(val) for val in raw]
        return self.processed_values

    def comma_list_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = raw[0].split(",")
        return self.processed_values


class Program:
    instructions = None
    ip = 0
    stop = False
    input = None
    output = None

    def parse_paramopcode(self, paramopcode):
        (raw_param, opcode) = divmod(paramopcode, 100)
        (d, c) = divmod(raw_param, 10)
        (d, b) = divmod(d, 10)
        (d, a) = divmod(d, 10)
        return (opcode, a, b, c)

    def get_param(self, value, param_mode):
        if param_mode == 0:  # Position mode
            return self.instructions[value]
        else:  # Immediate Mode
            return value

    def __str__(self):
        result = "ip: {}[{}]-{}".format(self.ip, self.instructions[self.ip], self.instructions)
        return result

    def __init__(self, instructions):
        self.instructions = instructions.copy()
        self.ip = 0
        self.output = []

    def evaluate_instruction(self):
        if (self.instructions[self.ip] == 99) or self.ip > len(self.instructions):
            self.stop = True
        else:
            paramopcode = self.instructions[self.ip]
            (opcode, a, b, c) = self.parse_paramopcode(paramopcode)

            if opcode == 1:
                self.opcode_1_add(b, c)
            elif opcode == 2:
                self.opcode_2_mult(b, c)
            elif opcode == 3:
                self.opcode_3_stor_input()
            elif opcode == 4:
                self.opcode_4_output(c)
            elif opcode == 5:
                self.opcode_5_jtrue(b, c)
            elif opcode == 6:
                self.opcode_6_jfalse(b, c)
            elif opcode == 7:
                self.opcode_7_lt(b, c)
            elif opcode == 8:
                self.opcode_8_eq(b, c)
            else:
                self.stop = True

    def opcode_8_eq(self, b, c):
        (reg1, reg2, reg3) = self.instructions[self.ip + 1:(self.ip + 4)]
        if self.get_param(reg1, c) == self.get_param(reg2, b):
            self.instructions[reg3] = 1
        else:
            self.instructions[reg3] = 0
        self.ip += 4

    def opcode_7_lt(self, b, c):
        (reg1, reg2, reg3) = self.instructions[self.ip + 1:(self.ip + 4)]
        if self.get_param(reg1, c) < self.get_param(reg2, b):
            self.instructions[reg3] = 1
        else:
            self.instructions[reg3] = 0
        self.ip += 4

    def opcode_6_jfalse(self, b, c):
        (reg1, reg2) = self.instructions[self.ip + 1:(self.ip + 3)]
        if self.get_param(reg1, c) == 0:
            self.ip = self.get_param(reg2, b)
        else:
            self.ip += 3

    def opcode_5_jtrue(self, b, c):
        (reg1, reg2) = self.instructions[self.ip + 1:(self.ip + 3)]
        if self.get_param(reg1, c) != 0:
            self.ip = self.get_param(reg2, b)
        else:
            self.ip += 3

    def opcode_4_output(self,c):
        reg1 = self.instructions[self.ip + 1]
        self.output.append(self.get_param(reg1,c))
        self.ip += 2

    def opcode_3_stor_input(self):
        reg1 = self.instructions[self.ip + 1]
        reg2 = self.input[0]
        self.instructions[reg1] = reg2
        self.ip += 2

    def opcode_2_mult(self, b, c):
        (reg1, reg2, reg3) = self.instructions[self.ip + 1:(self.ip + 4)]
        self.instructions[reg3] = self.get_param(reg1, c) * self.get_param(reg2, b)
        self.ip += 4

    def opcode_1_add(self, b, c):
        (reg1, reg2, reg3) = self.instructions[self.ip + 1:(self.ip + 4)]
        self.instructions[reg3] = self.get_param(reg1, c) + self.get_param(reg2, b)
        self.ip += 4

    def evaluate(self):
        while (not self.stop):
            self.evaluate_instruction()


if __name__ == '__main__':
    value_loader = LoadValues()
    values = value_loader.comma_list_to_intlist()
    int_val = [int(val) for val in values]
    print(int_val)
    init_prog = int_val.copy()
    my_prog = Program(init_prog)
    my_prog.input = [1]
    my_prog.evaluate()
    print(my_prog.output)

    init_prog = int_val.copy()
    my_prog = Program(init_prog)
    my_prog.input = [5]
    my_prog.evaluate()
    print(my_prog.output)
