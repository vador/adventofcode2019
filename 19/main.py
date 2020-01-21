from loadValues import LoadValues
from program import Program

import cProfile, pstats

lv = LoadValues("input")
output = lv.comma_list_to_intlist()
int_val = [int(val) for val in output]
my_prog = Program(int_val)
my_prog.logger.min_log_level = 2


pr = cProfile.Profile()
pr.enable()
#
cnt = 0
for x in range(50):
    print(x, "\t", end="")
    for y in range(50):
        tmp_prog = Program(int_val)
        tmp_prog.logger.min_log_level = 2
        tmp_prog.input = [x, y]
        tmp_prog.evaluate()
        print(tmp_prog.output[0], end="")
        if tmp_prog.output[0] == 1:
            cnt += 1
    print()
print(cnt)

pr.disable()
#pr.print_stats()
