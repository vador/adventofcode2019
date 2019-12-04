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

    def __str__(self):
        result = "ip: {}[{}]-{}".format(self.ip, self.instructions[self.ip], self.instructions)
        return result

    def __init__(self, instructions):
        self.instructions = instructions.copy()
        self.ip = 0

    def evaluate_instruction(self):
        if (self.instructions[self.ip] == 99) or (self.ip + 3) > len(self.instructions):
            self.stop = True
        else:
            (opcode, reg1, reg2, reg3) = self.instructions[self.ip:(self.ip + 4)]
            if opcode == 1:
                self.instructions[reg3] = self.instructions[reg1] + self.instructions[reg2]
            elif opcode == 2:
                self.instructions[reg3] = self.instructions[reg1] * self.instructions[reg2]
            else:
                self.stop = True
            self.ip += 4

    def evaluate(self):
        program = self.instructions
        ip = self.ip
        nb_val = len(self.instructions)
        while (not self.stop):
            self.evaluate_instruction()


def calibrate(values):
    values[1] = 12
    values[2] = 2
    return values


def find_noun_verb(values, noun, verb):

    new_prog = values.copy()
    new_prog[1] = noun
    new_prog[2] = verb
    my_prog = Program(new_prog)
    my_prog.evaluate()
    return my_prog.instructions[0]


if __name__ == '__main__':
    data = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,6,23,2,6,23,27,2,27,9,31,1,5,31,35,1,35,10,39,2,39,9,43,1,5,43,47,2,47,10,51,1,51,6,55,1,5,55,59,2,6,59,63,2,63,6,67,1,5,67,71,1,71,9,75,2,75,10,79,1,79,5,83,1,10,83,87,1,5,87,91,2,13,91,95,1,95,10,99,2,99,13,103,1,103,5,107,1,107,13,111,2,111,9,115,1,6,115,119,2,119,6,123,1,123,6,127,1,127,9,131,1,6,131,135,1,135,2,139,1,139,10,0,99,2,0,14,0"
    value_loader = LoadValues([data], False)
    #value_loader = LoadValues()
    values = value_loader.comma_list_to_intlist()
    int_val = [int(val) for val in values]
    print(int_val)
    init_prog = calibrate(int_val.copy())
    my_prog = Program(init_prog)
    my_prog.evaluate()
    print(my_prog)

    for noun in range(100):
        for verb in range(100):
            res = find_noun_verb(int_val, noun, verb)
            if (res == 19690720):
                print("Success !")
                print(noun, ":", verb, "=", res, "100*noun+verb", 100 * noun + verb)

                break
