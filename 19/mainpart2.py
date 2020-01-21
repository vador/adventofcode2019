from loadValues import LoadValues
from program import Program

import cProfile, pstats


VESSEL_SIZE = 100
lv = LoadValues("input")
output = lv.comma_list_to_intlist()
int_val = [int(val) for val in output]
my_prog = Program(int_val)
my_prog.logger.min_log_level = 0

def get_value(x,y):
    tmp_prog = Program(int_val)
    tmp_prog.logger.min_log_level = 2
    tmp_prog.input.append(x)
    tmp_prog.input.append(y)
    tmp_prog.evaluate()
    return tmp_prog.output[0]

def is_fitting_vessel(line):
    if line < VESSEL_SIZE-1:
        return False
    (xmin1, xmax1) = coords[line - VESSEL_SIZE + 1]
    (xmin2, xmax2) = coords[line]
    if xmax1 - xmin2 >= VESSEL_SIZE-1:
        return True
    return False


def find_next_line(line):
    # coords are at least as much
    (xminp, xmaxp) = coords[line - 1]
    (xmind, xmaxd) = coords[line - 2]
    res = 0
    delta = xminp - xmind - 1
    while True:
        res = get_value(xminp + delta, line)
        if res == 1:
            break
        delta += 1
    xmin = xminp + delta
    res = 1
    delta = xmaxp - xmaxd - 1
    res = get_value(xmaxp + delta, line)
    if res == 0:
        print("Warning - backtrack")
        delta = 0

    while True:
        res = get_value(xmaxp + delta, line)
        if res == 0:
            break
        delta += 1
    xmax = xmaxp + delta - 1
    return (xmin, xmax)

pr = cProfile.Profile()
pr.enable()
#
coords = [(0,0)] * 25
xmin = 21
xmax = 24
print(xmin, xmax)
coords.append((xmin, xmax))
xmin = 22
xmax = 28
print(xmin, xmax)
coords.append((xmin, xmax))

print(coords)
print(coords[25])
cur_line = 27
while True:
    print("line : ", cur_line, " ", end="")
    (xmin, xmax) = find_next_line(cur_line)
    coords.append((xmin, xmax))
    print((xmin, xmax), " : ", end="")
    res = is_fitting_vessel(cur_line)
    print(res)
    if res == True:
        break
    cur_line += 1

(x_pos, y_pos) = (xmin, cur_line - VESSEL_SIZE +1)
print(x_pos, y_pos)
print(x_pos * 10000 + y_pos)

pr.disable()
#pr.print_stats()
