from program import Program
from loadValues import LoadValues
from arcade import Arcade

if __name__ == '__main__':
    lv = LoadValues("input")
    output = lv.comma_list_to_intlist()
    int_val = [int(val) for val in output]
    my_prog = Program(int_val)
    arc = Arcade()

    my_prog.logger.min_log_level = 2
    my_prog_iter = my_prog.__iter__()
    output = []

    for val in my_prog_iter:
        output.append(val)
        if len(output) >= 3:
            x = output.pop(0)
            y = output.pop(0)
            tile_id = output.pop(0)
            arc.set_tile((x,y), tile_id)
    print(arc.count_blocks())
