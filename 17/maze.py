from program import Program
from loadValues import LoadValues
from scaffoldMap import ScaffoldMap


def get_map(prog):
    map = []
    line = []
    for val in prog:
        if val == 10:
            print()
            # line.append('.')
            map.append("".join(line))
            # line = ['.']
            line = []
        else:
            print(chr(val), end="")
            line.append(chr(val))
    print("Last value : ", val)
    return map


if __name__ == '__main__':
    lv = LoadValues("input")
    output = lv.comma_list_to_intlist()
    int_val = [int(val) for val in output]

    int_val[0] = 2
    my_prog = Program(int_val)
    my_prog.logger.min_log_level = 2

    lv2 = LoadValues("input2")
    my_sm = ScaffoldMap()
    my_sm.scaffoldMap = lv2.strip_lines()

    intersects = my_sm.get_intersections()
    print(intersects)
    result = sum([(i * j) for (i, j) in intersects])
    print(result)

    nl = [10]
    A = ",".join(["R", "8", "L", "10", "L", "12", "R", "4"])
    B = ",".join(["R", "8", "L", "12", "R", "4", "R", "4"])
    C = ",".join(["R", "8", "L", "10", "R", "8"])
    seq = ",".join(["A", "B", "A", "C", "A", "B", "C", "B", "C", "B"])
    A = list(map(ord, A))
    B = list(map(ord, B))
    C = list(map(ord, C))
    seq = list(map(ord, seq))
    params = seq + nl + A + nl + B + nl + C + nl

    my_prog.input += params
    my_prog.input += [ord("n"), 10]
    print(my_prog.input)
    mm_map = get_map(my_prog)
