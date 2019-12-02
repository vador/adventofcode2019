import sys
import re
import collections
import math
import heapq


def get_values():
    with open('./input' if len(sys.argv) < 2 else sys.argv[1]) as f:
        data = list(f)
        datab = [int(val) for val in data]
 #   bots = [tuple(map(int, list(re.findall(r'-?\d+', ln)))) for ln in data]
    return datab

def calc_unit_fuel(val):
    return math.floor(val/3)-2

def calc_full_fuel(val):
    unit_fuel = calc_unit_fuel(val)
    if unit_fuel <= 0:
        return 0
    else:
        return unit_fuel + calc_full_fuel(unit_fuel)

if __name__ == '__main__':
    values = get_values()
    fuel = [calc_unit_fuel(val) for val in values]
    print(fuel)
    print(sum(fuel))
    full_fuel  = [calc_full_fuel(val) for val in values]
    print(full_fuel)
    print(sum(full_fuel))
