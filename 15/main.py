from program import Program
from loadValues import LoadValues
from spaceMap import SpaceMap
from spaceMap import Explorer

if __name__ == '__main__':
    lv = LoadValues("input")
    output = lv.comma_list_to_intlist()
    int_val = [int(val) for val in output]
    my_prog = Program(int_val)
    my_prog.logger.min_log_level = 2
    my_sp = SpaceMap()
    my_explorer = Explorer(my_sp, my_prog)
    my_explorer.explore()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(my_explorer.spacemap.display_hull())
    print("===")

    distances = my_explorer.bfs((0,0))
    print(distances[my_explorer.oxygen_pos])
    distances = my_explorer.bfs(my_explorer.oxygen_pos)
    max = 0
    for dist in distances.values():
        if dist > max:
            max = dist
    print(max)