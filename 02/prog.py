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

def evaluate(program):
    ip = 0
    stop = False
    nb_val = len(program)
    while (not stop):
        if (program[ip] == 99) or (ip+3)>nb_val:
            #print("Program stopped at ip :", ip, "[", program[ip], "]")
            stop = True
        else:
            (opcode,reg1,reg2,reg3) = program[ip:(ip+4)]
            if opcode == 1:
                program[reg3] = program[reg1] + program[reg2]
            elif opcode == 2:
                program[reg3] = program[reg1] * program[reg2]
            else:
                #print("Program stopped at ip :", ip, "[", program[ip], "]")
                stop = True
            ip +=4
    #print("Program finished at ip :", ip, "[", program[ip], "]")
    return program

def calibrate(values):
    values[1] = 12
    values[2] = 2
    return values

def find_noun_verb(values, noun, verb):
    new_prog = values.copy()
    new_prog[1] = noun
    new_prog[2] = verb
    res = evaluate(new_prog)
    return res[0]

if __name__ == '__main__':
    values = get_values()
    int_val = [int(val) for val in values]
    print(int_val)
    init_prog = calibrate(int_val.copy())
    result = evaluate(init_prog)
    print(result[0])

    for noun in range(100):
        for verb in range(100):
            res = find_noun_verb(int_val, noun, verb)
            if (res == 19690720):
                print("Success !")
                print(noun, ":", verb, "=", res, "100*noun+verb", 100*noun+verb)

                break
