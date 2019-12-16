import sys
import re
import collections
import math
import heapq
import itertools


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

    def output_value(self, val):
        self.output.append(val)

    def get_input_value(self):
        return self.input.pop(0)

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
        self.input = []

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

    def opcode_4_output(self, c):
        reg1 = self.instructions[self.ip + 1]
        val = self.get_param(reg1, c)
        self.output_value(val)
        self.ip += 2

    def opcode_3_stor_input(self):
        reg1 = self.instructions[self.ip + 1]
        reg2 = self.get_input_value()
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
        return

    def __iter__(self):
        return self

    def __next__(self):
        while (not self.stop):
            self.evaluate_instruction()
            if len(self.output) >0:
                return self.output.pop(0)
        raise StopIteration

def run_amplifier_stage(phase, input, program):
    init_prog = program.copy()
    my_prog = Program(init_prog)
    my_prog.input = [phase, input]
    my_prog_iter = my_prog.__iter__()
    val = my_prog_iter.__next__()
    my_prog_iter = None
    return val

def run_full_amplification(phase_list, program):
    buf = 0
    for phase in phase_list:
        buf = run_amplifier_stage(phase, buf, program)
    return buf

def phase2_amplification(phase_list, program):
    stage_list = []
    for i in range(5):
        stage = Program(program.copy())
        stage.input.append(phase_list[i])
        stage_list.append(stage.__iter__())
    stage_list[0].input.append(0)
    i = 0
    while True:
        try:
            val = stage_list[i].__next__()
            i = (i + 1) % 5
            print("Stage: ", i, " ", val)
            stage_list[i].input.append(val)
        except StopIteration:
            return val

if __name__ == '__main__':
    value_loader = LoadValues("input")
    values = value_loader.comma_list_to_intlist()
    int_val = [int(val) for val in values]
    print(int_val)

    max_output = -1
    best_phase_list = None
    for phase_list in itertools.permutations([0, 1, 2, 3, 4], 5):
        output = run_full_amplification(phase_list, int_val)
        if output > max_output:
            max_output = output
            best_phase_list = phase_list

    print("Best : ", best_phase_list, max_output)

    max_output = -1
    best_phase_list = None
    for phase_list in itertools.permutations([5,6,7,8,9], 5):
        output = phase2_amplification(phase_list, int_val)
        if output > max_output:
            max_output = output
            best_phase_list = phase_list
    print("Best Phase 2: ", best_phase_list, max_output)

