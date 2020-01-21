from graph import Graph

from loadValues import LoadValues

lv = LoadValues("input")
maze = lv.raw_values
my_graph = Graph()

my_graph.build_maze(maze)

print(my_graph.maze)
print(my_graph.boundaries_ext, my_graph.boundaries_int)
print(my_graph.graph)
print(my_graph.bfs())
print(my_graph.bfs_alt())
