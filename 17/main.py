from program import Program
from loadValues import LoadValues
from scaffoldMap import ScaffoldMap

def get_map(prog):
    map = []
    line = []
    for val in prog:
        if val == 10:
            print()
            #line.append('.')
            map.append("".join(line))
            #line = ['.']
            line = []
        else:
            print(chr(val), end="")
            line.append(chr(val))
    return map

if __name__ == '__main__':
    lv = LoadValues("input")
    output = lv.comma_list_to_intlist()
    int_val = [int(val) for val in output]
    my_prog = Program(int_val)
    my_prog.logger.min_log_level = 2
    my_sm = ScaffoldMap()


#    map = get_map(my_prog)
#    my_sm.scaffoldMap = map
    lv = LoadValues("input2")
    my_sm.scaffoldMap = lv.strip_lines()

    intersects = my_sm.get_intersections()
    print(intersects)
    result = sum([(i*j) for (i,j) in intersects])
    print(result)