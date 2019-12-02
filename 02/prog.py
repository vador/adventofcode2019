import sys
import re
import collections
import math
import heapq


def get_values():
    with open('./input' if len(sys.argv) < 2 else sys.argv[1]) as f:
        data = list(f)
        datab = process_comma_list(data)
    return datab


def process_comma_list(data):
    return data[0].split(",")


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
        if (self.instructions[self.ip] == 99) or (self.ip+3)> len(self.instructions):
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
    values = get_values()
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
