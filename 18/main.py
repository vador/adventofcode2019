from loadValues import LoadValues
from mazeKeys import Graph
import cProfile, pstats

lv = LoadValues("input")
maze = lv.strip_lines()
my_graph = Graph()
# my_graph.build_maze(maze)
# print(my_graph.graph)
# print(my_graph.key_pos)
# print(my_graph.door_pos)
# print(my_graph.entrance)

# print(my_graph.find_reachable_keys(my_graph.entrance, []))
# print(my_graph.find_reachable_keys((17,1), ['a']))
# print(my_graph.find_reachable_keys((11,1), ['a','b']))

# print(my_graph.find_best_path(my_graph.entrance, [], 0))

# print(my_graph.find_reachable_keys((1,3), ['a','b', 'c', 'd', 'e']))
pr = cProfile.Profile()

# pr.enable()
#
# print(my_graph.find_best_path_from_entrance())
#
# pr.disable()
# pr.print_stats()

# pr2 = cProfile.Profile()
#
# pr2.enable()
# print(my_graph.find_best_path_dijkstra())
# pr2.disable()
# pr2.print_stats()

my_graph.build_maze_4_bots(maze)
print(my_graph.graph)
print(my_graph.key_pos)
print(my_graph.door_pos)
print(my_graph.entrance)
#for key in my_graph.key_path.keys():
print(my_graph.key_path)

print(my_graph.find_best_path_dijkstra_4_bots())